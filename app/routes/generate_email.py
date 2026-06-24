"""
Route handler for POST /generate-email.
Thin handler — all logic lives in email_service.
"""

from fastapi import APIRouter, Request
from app.models.schemas import GenerateEmailRequest, GenerateEmailResponse
from app.services.email_service import generate_email

router = APIRouter()


@router.post(
    "/generate-email",
    response_model=GenerateEmailResponse,
    summary="Generate Professional Email",
    description=(
        "Accepts a context description and optional parameters, then generates a complete "
        "professional email with a subject line and body. Supports multiple tones such as "
        "'formal', 'friendly', and 'professional'. Powered by Google Gemini."
    ),
    response_description="A JSON object containing the email subject, body, and tone used.",
    tags=["Email"],
    responses={
        200: {
            "description": "Email generated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "subject": "Follow-Up: Product Demo & Next Steps",
                        "body": "Dear Mr. Sharma,\n\nThank you for joining our product demo...",
                        "tone": "professional",
                        "request_id": "d5f4g3c2-3456-7890-cdef-012345678901",
                    }
                }
            },
        },
        422: {"description": "Validation error — missing or invalid fields."},
        500: {"description": "Internal server error from the AI model."},
    },
)
async def generate_email_endpoint(
    body: GenerateEmailRequest, request: Request
) -> GenerateEmailResponse:
    """
    Generate a professional email using Google Gemini.

    - **context**: A description of what the email should be about.
    - **tone**: Desired tone — 'formal', 'friendly', or 'professional' (default).
    - **recipient_name**: Optional name for the recipient greeting.
    - **sender_name**: Optional name for the email sign-off.
    """
    request_id: str = getattr(request.state, "request_id", "unknown")
    return await generate_email(body, request_id)