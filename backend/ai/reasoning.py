from ai.agent import run_diagnosis
from models.investigation import InvestigationPayload


def analyze_cluster_state(investigation: InvestigationPayload):
    return run_diagnosis(investigation)
