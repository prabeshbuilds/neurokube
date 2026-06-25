from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    root_cause: str
    explanation: str
    fix: str
    kubectl_command: str
    prevention_recommendation: str = ""
    confidence: int = Field(ge=0, le=100)
    confidence_reasoning: str = ""


class LLMDiagnosisResponse(BaseModel):
    """Expected JSON shape from the LLM."""

    root_cause: str
    explanation: str
    fix: str
    kubectl_commands: list[str] = Field(default_factory=list)
    prevention_recommendation: str = ""
    confidence: int = Field(default=50, ge=0, le=100)
    confidence_reasoning: str = ""
