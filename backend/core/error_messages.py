"""User-friendly error messages for API responses."""

from ai.llm_client import LLMClientError


def friendly_llm_error(error: LLMClientError) -> str:
    message = str(error).lower()
    if "not configured" in message or "openrouter_api_key" in message:
        return (
            "AI diagnosis is not configured.\n"
            "Please set OPENROUTER_API_KEY in the backend environment."
        )
    if "timed out" in message or "timeout" in message:
        return (
            "AI reasoning timed out.\n"
            "Please try again or choose a faster OPENROUTER_MODEL."
        )
    if "failed after" in message:
        return (
            "OpenRouter request failed.\n"
            "Please verify:\n"
            "- OPENROUTER_API_KEY is valid\n"
            "- OPENROUTER_MODEL is available\n"
            "- network access to OpenRouter"
        )
    return f"AI diagnosis unavailable: {error}"


def friendly_auth_error(message: str) -> str:
    if "missing" in message.lower() or "required" in message.lower():
        return "Please sign in again to run an investigation."
    if "invalid" in message.lower() or "expired" in message.lower():
        return "Your session expired. Please sign in again."
    return message
