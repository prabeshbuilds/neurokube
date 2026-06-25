import time

import httpx
from loguru import logger

from core.config import settings


class LLMClientError(Exception):
    pass


class LLMClient:
    """OpenRouter client using HTTPX with retries and timeout handling."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.openrouter_api_key
        self.model = model if model is not None else settings.openrouter_model
        self.base_url = (base_url or settings.openrouter_base_url).rstrip("/")
        self.timeout = timeout if timeout is not None else settings.openrouter_timeout
        self.max_retries = max_retries if max_retries is not None else settings.openrouter_max_retries

    def chat_completion(self, messages: list[dict[str, str]]) -> str:
        if not self.api_key:
            raise LLMClientError("OPENROUTER_API_KEY is not configured")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-kubernetes-agent.local",
            "X-Title": "AI Kubernetes Agent",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        last_error = "Unknown error"
        for attempt in range(1, self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    logger.info("LLM response received (model={})", self.model)
                    return content

                last_error = f"HTTP {response.status_code}: {response.text[:300]}"
                logger.warning(
                    "OpenRouter request failed (attempt {}/{}): {}",
                    attempt,
                    self.max_retries,
                    last_error,
                )
            except httpx.TimeoutException:
                last_error = f"Request timed out after {self.timeout}s"
                logger.warning(
                    "OpenRouter timeout (attempt {}/{}): {}",
                    attempt,
                    self.max_retries,
                    last_error,
                )
            except httpx.HTTPError as exc:
                last_error = str(exc)
                logger.warning(
                    "OpenRouter HTTP error (attempt {}/{}): {}",
                    attempt,
                    self.max_retries,
                    last_error,
                )

            if attempt < self.max_retries:
                time.sleep(2 ** (attempt - 1))

        raise LLMClientError(f"OpenRouter request failed after {self.max_retries} attempts: {last_error}")
