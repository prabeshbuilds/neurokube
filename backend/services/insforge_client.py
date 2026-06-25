import httpx
from loguru import logger

from core.config import settings


class InsForgeClientError(Exception):
    pass


class InsForgeClient:
    """InsForge REST client for auth validation and investigation persistence."""

    def __init__(self) -> None:
        self.base_url = settings.insforge_base_url.rstrip("/")
        self.anon_key = settings.insforge_anon_key

    def validate_token(self, access_token: str) -> dict:
        if not access_token:
            raise InsForgeClientError("Missing access token")

        url = f"{self.base_url}/api/auth/sessions/current"
        headers = self._auth_headers(access_token)

        try:
            with httpx.Client(timeout=15) as client:
                response = client.get(url, headers=headers)
        except httpx.HTTPError as exc:
            raise InsForgeClientError("Failed to validate session") from exc

        if response.status_code != 200:
            logger.warning("InsForge auth validation failed: {}", response.status_code)
            raise InsForgeClientError("Invalid or expired session")

        data = response.json()
        user = data.get("user")
        if not user:
            raise InsForgeClientError("Invalid session response")

        return user

    def update_investigation(
        self,
        access_token: str,
        investigation_id: str,
        payload: dict,
    ) -> None:
        url = (
            f"{self.base_url}/api/database/records/investigations"
            f"?id=eq.{investigation_id}"
        )
        headers = {
            **self._auth_headers(access_token),
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        body = {**payload, "updated_at": payload.get("updated_at") or _utc_now()}

        try:
            with httpx.Client(timeout=15) as client:
                response = client.patch(url, headers=headers, json=body)
        except httpx.HTTPError as exc:
            logger.warning("Failed to update investigation {}: {}", investigation_id, exc)
            return

        if response.status_code >= 400:
            logger.warning(
                "Investigation update failed ({}): {}",
                response.status_code,
                response.text[:200],
            )

    def _auth_headers(self, access_token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {access_token}"}


def _utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()
