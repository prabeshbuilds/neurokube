from pydantic import BaseModel


class Diagnosis(BaseModel):
    """Placeholder model for future AI diagnosis results."""

    root_cause: str | None = None
    suggested_fix: str | None = None
