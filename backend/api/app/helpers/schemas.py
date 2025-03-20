"""
The API schemas.
"""
from typing import Optional

from pydantic import BaseModel, Field


class TemplateRequest(BaseModel):
    """The schema used for the render template endpoint."""

    template: str
    variables: Optional[str] = Field(default="")  # Can be empty, YAML, or JSON string


class APIResponseSchema(BaseModel):
    """The schema used for the API response."""

    error: bool = Field(
        description="Whether an error occurred during the check", examples=[False]
    )
    msg: str | None
    results: str | None = Field(default=None)


class APIErrorResponseSchema(BaseModel):
    """The error schema used for the API error response."""

    error: bool = Field(description="Whether an error occurred", examples=[True])
    detail: str = Field(description="The error message")
    extra: list[dict] = Field(
        description="The parameter and error this exception relates to"
    )
