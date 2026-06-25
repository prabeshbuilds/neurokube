from models.diagnosis import Diagnosis, LLMDiagnosisResponse


class FixRecommendationEngine:
    """Turns LLM output into actionable fix recommendations."""

    def build(self, llm_response: LLMDiagnosisResponse) -> Diagnosis:
        kubectl_command = self._format_kubectl_commands(llm_response.kubectl_commands)

        return Diagnosis(
            root_cause=llm_response.root_cause.strip(),
            explanation=llm_response.explanation.strip(),
            fix=llm_response.fix.strip(),
            kubectl_command=kubectl_command,
            prevention_recommendation=llm_response.prevention_recommendation.strip(),
            confidence=llm_response.confidence,
            confidence_reasoning=llm_response.confidence_reasoning.strip(),
        )

    @staticmethod
    def _format_kubectl_commands(commands: list[str]) -> str:
        cleaned = [cmd.strip() for cmd in commands if cmd.strip()]
        if not cleaned:
            return "kubectl get pods -A"
        if len(cleaned) == 1:
            return cleaned[0]
        return "\n".join(f"{index + 1}. {cmd}" for index, cmd in enumerate(cleaned))
