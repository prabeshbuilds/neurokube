from fastapi import APIRouter, Header, HTTPException
from loguru import logger

from core.config import settings
from core.error_messages import friendly_auth_error, friendly_llm_error
from kubernetes.cluster_config import cluster_contexts_to_dict, list_clusters
from models.clusters import ClusterInfo, ClusterListResponse
from services.insforge_client import InsForgeClient, InsForgeClientError

router = APIRouter(tags=["clusters"])
insforge_client = InsForgeClient()


@router.get("/clusters", response_model=ClusterListResponse)
def get_clusters(
    authorization: str | None = Header(default=None),
) -> ClusterListResponse:
    access_token = _extract_bearer_token(authorization)

    try:
        insforge_client.validate_token(access_token)
    except InsForgeClientError as exc:
        raise HTTPException(status_code=401, detail=friendly_auth_error(str(exc))) from exc

    contexts, error = list_clusters(kubeconfig_path=settings.kubeconfig_path)
    clusters = [ClusterInfo.model_validate(item) for item in cluster_contexts_to_dict(contexts)]

    return ClusterListResponse(
        status="success" if not error else "error",
        clusters=clusters,
        error=error,
    )


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Please sign in again to view clusters.",
        )
    return authorization.removeprefix("Bearer ").strip()
