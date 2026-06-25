from models.diagnosis import Diagnosis
from models.investigation import InvestigationPayload


class ConfidenceEngine:
    """Adjusts and validates confidence based on evidence quality."""

    def score(
        self,
        diagnosis: Diagnosis,
        investigation: InvestigationPayload,
    ) -> Diagnosis:
        confidence = max(0, min(100, diagnosis.confidence))
        reasoning_parts = []

        if diagnosis.confidence_reasoning:
            reasoning_parts.append(diagnosis.confidence_reasoning)

        evidence_signals = self._count_evidence_signals(investigation)
        if evidence_signals >= 3:
            boost = min(10, evidence_signals * 2)
            confidence = min(100, confidence + boost)
            reasoning_parts.append(
                f"Confidence boosted because {evidence_signals} independent evidence sources align."
            )
        elif evidence_signals == 0 and self._cluster_looks_healthy(investigation):
            confidence = max(confidence, 85)
            reasoning_parts.append(
                "High confidence because no problematic pods, events, deployments, or network issues were found."
            )
        elif evidence_signals == 1:
            confidence = max(0, confidence - 10)
            reasoning_parts.append(
                "Confidence reduced slightly because only one evidence source indicates a problem."
            )

        diagnosis.confidence = confidence
        diagnosis.confidence_reasoning = " ".join(reasoning_parts).strip()
        return diagnosis

    @staticmethod
    def _count_evidence_signals(investigation: InvestigationPayload) -> int:
        signals = 0
        if investigation.pods.problematic_pods:
            signals += 1
        if investigation.logs.entries:
            signals += 1
        if investigation.events.findings:
            signals += 1
        if investigation.deployments.problematic_deployments:
            signals += 1
        if investigation.network.findings:
            signals += 1
        return signals

    @staticmethod
    def _cluster_looks_healthy(investigation: InvestigationPayload) -> bool:
        return (
            investigation.pods.healthy
            and not investigation.logs.entries
            and not investigation.events.findings
            and investigation.deployments.healthy
            and investigation.network.healthy
        )
