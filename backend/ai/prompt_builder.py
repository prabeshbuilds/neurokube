import json

from models.investigation import InvestigationPayload

SYSTEM_PROMPT = """You are a Senior Kubernetes SRE performing incident triage.

Your job is to analyze Kubernetes troubleshooting evidence and produce a precise diagnosis.
Correlate pod status, logs, events, deployment health, and networking findings together.
Do not summarize logs blindly — identify the underlying root cause.

Rules:
- Be specific and actionable. Name resources (pods, deployments, services, namespaces).
- Prefer the most likely root cause supported by multiple evidence sources.
- Provide practical kubectl commands a beginner can run.
- Avoid vague advice like "check the logs" without saying what to look for.
- If the cluster appears healthy, state that clearly with high confidence.

You MUST respond with valid JSON only (no markdown), using this exact schema:
{
  "root_cause": "One concise sentence stating the root cause",
  "explanation": "2-4 sentences correlating evidence from pods, logs, events, deployments, and network",
  "fix": "Clear step-by-step fix a beginner can follow",
  "kubectl_commands": ["kubectl command 1", "kubectl command 2"],
  "prevention_recommendation": "How to prevent this issue in the future",
  "confidence": 85,
  "confidence_reasoning": "Why this confidence level, citing specific evidence"
}

confidence must be an integer from 0 to 100."""


class PromptBuilder:
    """Builds structured prompts for Kubernetes troubleshooting."""

    def build(self, investigation: InvestigationPayload) -> list[dict[str, str]]:
        evidence = investigation.model_dump(mode="json")
        user_content = (
            "Analyze the following Kubernetes investigation evidence and return your diagnosis as JSON.\n\n"
            f"EVIDENCE:\n{json.dumps(evidence, indent=2)}"
        )

        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
