from fastapi import APIRouter, Header, HTTPException
from loguru import logger

from ai.agent import run_diagnosis
from ai.llm_client import LLMClientError
from core.error_messages import friendly_auth_error, friendly_llm_error
from models.investigation import InvestigateRequest, InvestigateResponse, InvestigationPayload
from services.insforge_client import InsForgeClient, InsForgeClientError
from services.investigation import InvestigationError, is_cluster_healthy, run_investigation

router = APIRouter(tags=["investigation"])
insforge_client = InsForgeClient()


@router.post("/investigate", response_model=InvestigateResponse)
def investigate_cluster(
    body: InvestigateRequest,
    authorization: str | None = Header(default=None),
) -> InvestigateResponse:
    access_token = _extract_bearer_token(authorization)

    try:
        insforge_client.validate_token(access_token)
    except InsForgeClientError as exc:
        raise HTTPException(status_code=401, detail=friendly_auth_error(str(exc))) from exc

    investigation_id = body.investigation_id
    cluster_context = body.cluster_context.strip()
    if not cluster_context:
        raise HTTPException(
            status_code=400,
            detail="Please select a Kubernetes cluster before investigating.",
        )

    def on_progress(step: str, label: str) -> None:
        insforge_client.update_investigation(
            access_token,
            investigation_id,
            {
                "status": "running",
                "progress_step": step,
                "progress_label": label,
                "cluster_context": cluster_context,
            },
        )

    try:
        on_progress("checking_pods", "Checking Pods")
        investigation = run_investigation(
            cluster_context=cluster_context,
            on_progress=on_progress,
        )
    except InvestigationError as exc:
        logger.warning("Investigation error: {}", exc.message)
        insforge_client.update_investigation(
            access_token,
            investigation_id,
            {
                "status": "failed",
                "progress_label": "Investigation failed",
                "cluster_context": cluster_context,
            },
        )
        raise HTTPException(status_code=502, detail=exc.message) from exc
    except Exception as exc:
        logger.exception("Investigation failed")
        insforge_client.update_investigation(
            access_token,
            investigation_id,
            {
                "status": "failed",
                "progress_label": "Investigation failed",
                "cluster_context": cluster_context,
            },
        )
        raise HTTPException(
            status_code=500,
            detail="Investigation failed unexpectedly. Check backend logs for details.",
        ) from exc

    try:
        on_progress("ai_reasoning", "AI Reasoning")
        diagnosis = run_diagnosis(investigation)
        on_progress("root_cause_found", "Root Cause Found")
    except LLMClientError as exc:
        logger.error("AI diagnosis failed: {}", exc)
        insforge_client.update_investigation(
            access_token,
            investigation_id,
            {"status": "failed", "progress_label": "AI diagnosis failed"},
        )
        raise HTTPException(status_code=503, detail=friendly_llm_error(exc)) from exc
    except Exception as exc:
        logger.exception("AI diagnosis failed")
        insforge_client.update_investigation(
            access_token,
            investigation_id,
            {"status": "failed", "progress_label": "AI diagnosis failed"},
        )
        raise HTTPException(
            status_code=500,
            detail="AI diagnosis failed unexpectedly. Check backend logs for details.",
        ) from exc

    namespace = _extract_namespace(investigation)
    healthy = is_cluster_healthy(investigation)
    insforge_client.update_investigation(
        access_token,
        investigation_id,
        {
            "status": "completed",
            "progress_step": "root_cause_found",
            "progress_label": "Root Cause Found",
            "root_cause": diagnosis.root_cause,
            "namespace": namespace,
            "confidence": diagnosis.confidence,
            "cluster_context": cluster_context,
            "diagnosis": diagnosis.model_dump(mode="json"),
            "investigation": investigation.model_dump(mode="json"),
        },
    )

    return InvestigateResponse(
        status="success",
        investigation=investigation,
        diagnosis=diagnosis,
        cluster_healthy=healthy,
        cluster_context=cluster_context,
    )


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Please sign in again to run an investigation.",
        )
    return authorization.removeprefix("Bearer ").strip()


def _extract_namespace(investigation: InvestigationPayload) -> str:
    if investigation.pods.problematic_pods:
        return investigation.pods.problematic_pods[0].namespace
    if investigation.deployments.problematic_deployments:
        return investigation.deployments.problematic_deployments[0].namespace
    if investigation.network.findings:
        return investigation.network.findings[0].namespace
    if investigation.events.findings:
        return investigation.events.findings[0].namespace
    return "cluster-wide"
