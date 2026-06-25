import json
import re

from loguru import logger

from ai.llm_client import LLMClient, LLMClientError
from ai.prompt_builder import PromptBuilder
from models.diagnosis import Diagnosis, LLMDiagnosisResponse
from models.investigation import InvestigationPayload


class RootCauseAnalyzer:
    """Correlates investigation evidence via LLM reasoning."""

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prompt_builder = prompt_builder or PromptBuilder()

    def analyze(self, investigation: InvestigationPayload) -> LLMDiagnosisResponse:
        messages = self.prompt_builder.build(investigation)
        raw_response = self.llm_client.chat_completion(messages)
        return self._parse_response(raw_response)

    def _parse_response(self, raw_response: str) -> LLMDiagnosisResponse:
        cleaned = self._extract_json(raw_response)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse LLM JSON: {}", raw_response[:500])
            raise LLMClientError("LLM returned invalid JSON") from exc

        return LLMDiagnosisResponse.model_validate(data)

    @staticmethod
    def _extract_json(text: str) -> str:
        text = text.strip()
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fence_match:
            return fence_match.group(1)

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]

        return text
