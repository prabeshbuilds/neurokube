from loguru import logger

from ai.confidence_engine import ConfidenceEngine
from ai.fix_recommendation import FixRecommendationEngine
from ai.llm_client import LLMClientError
from ai.root_cause_analyzer import RootCauseAnalyzer
from models.diagnosis import Diagnosis
from models.investigation import InvestigationPayload


class AIKubernetesAgent:
    """Senior Kubernetes SRE agent — reasons over investigation evidence."""

    def __init__(self) -> None:
        self.root_cause_analyzer = RootCauseAnalyzer()
        self.fix_engine = FixRecommendationEngine()
        self.confidence_engine = ConfidenceEngine()

    def diagnose(self, investigation: InvestigationPayload) -> Diagnosis:
        logger.info("Starting AI diagnosis")

        llm_response = self.root_cause_analyzer.analyze(investigation)
        diagnosis = self.fix_engine.build(llm_response)
        diagnosis = self.confidence_engine.score(diagnosis, investigation)

        logger.info(
            "AI diagnosis complete (confidence={}%): {}",
            diagnosis.confidence,
            diagnosis.root_cause[:80],
        )
        return diagnosis


def run_diagnosis(investigation: InvestigationPayload) -> Diagnosis:
    return AIKubernetesAgent().diagnose(investigation)
