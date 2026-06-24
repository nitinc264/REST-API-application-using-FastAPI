"""
Pydantic v2 request and response schemas for all API endpoints.
All fields include descriptions for Swagger/OpenAPI documentation.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ── Summarize ──────────────────────────────────────────────────────────────────

class SummarizeRequest(BaseModel):
    """Request body for the /summarize endpoint."""

    text: str = Field(
        ...,
        min_length=20,
        max_length=10000,
        description="The text content to be summarized.",
        examples=["Artificial intelligence is transforming industries worldwide..."],
    )
    max_length: Optional[int] = Field(
        default=150,
        ge=30,
        le=500,
        description="Target maximum length of the summary in words.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Artificial intelligence (AI) is transforming industries across the globe. From healthcare to finance, AI-powered tools are enabling faster decisions, better predictions, and more personalized experiences. Machine learning models are now capable of diagnosing diseases, detecting fraud, and even writing code.",
                "max_length": 60,
            }
        }
    }


class SummarizeResponse(BaseModel):
    """Response body for the /summarize endpoint."""

    summary: str = Field(..., description="The generated summary of the input text.")
    original_length: int = Field(..., description="Word count of the original input text.")
    summary_length: int = Field(..., description="Word count of the generated summary.")
    request_id: Optional[str] = Field(None, description="Unique ID for this request.")


# ── Translate ──────────────────────────────────────────────────────────────────

class TranslateRequest(BaseModel):
    """Request body for the /translate endpoint."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The text content to be translated.",
        examples=["Hello, how are you?"],
    )
    target_language: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="The language to translate into (e.g., 'French', 'Spanish', 'Hindi').",
        examples=["French"],
    )
    source_language: Optional[str] = Field(
        default="auto-detect",
        description="The source language. Defaults to auto-detection.",
        examples=["English"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Hello, how are you?",
                "target_language": "French",
                "source_language": "English",
            }
        }
    }


class TranslateResponse(BaseModel):
    """Response body for the /translate endpoint."""

    translated_text: str = Field(..., description="The translated text.")
    source_language: str = Field(..., description="The detected or specified source language.")
    target_language: str = Field(..., description="The target language used for translation.")
    request_id: Optional[str] = Field(None, description="Unique ID for this request.")


# ── Generate Email ─────────────────────────────────────────────────────────────

class GenerateEmailRequest(BaseModel):
    """Request body for the /generate-email endpoint."""

    context: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="A description of what the email should be about.",
        examples=["Follow up with a client after a product demo, express interest in next steps."],
    )
    tone: Optional[str] = Field(
        default="professional",
        description="Desired tone of the email (e.g., 'formal', 'friendly', 'professional').",
        examples=["formal"],
    )
    recipient_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Name of the email recipient.",
        examples=["Mr. Sharma"],
    )
    sender_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Name of the email sender.",
        examples=["Nitin Chauhan"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "context": "Follow up with a client after a product demo, express interest in next steps.",
                "tone": "professional",
                "recipient_name": "Mr. Sharma",
                "sender_name": "Nitin Chauhan",
            }
        }
    }


class GenerateEmailResponse(BaseModel):
    """Response body for the /generate-email endpoint."""

    subject: str = Field(..., description="The generated email subject line.")
    body: str = Field(..., description="The full generated email body.")
    tone: str = Field(..., description="The tone used when generating the email.")
    request_id: Optional[str] = Field(None, description="Unique ID for this request.")


# ── Error ──────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Standardized error response returned on all exceptions."""

    error: bool = Field(default=True, description="Always true for error responses.")
    message: str = Field(..., description="Human-readable error message.")
    detail: Optional[str] = Field(None, description="Additional technical detail about the error.")
    request_id: Optional[str] = Field(None, description="Unique ID of the failed request.")