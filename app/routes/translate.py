"""
Route handler for POST /translate.
Thin handler — all logic lives in translate_service.
"""

from fastapi import APIRouter, Request
from app.models.schemas import TranslateRequest, TranslateResponse
from app.services.translate_service import translate_text

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate Text",
    description=(
        "Accepts text and a target language and returns an accurate AI-generated translation. "
        "Supports any language supported by Google Gemini. "
        "Source language is auto-detected if not specified."
    ),
    response_description="A JSON object containing the translated text and language metadata.",
    tags=["NLP"],
    responses={
        200: {
            "description": "Translation completed successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "translated_text": "Bonjour, comment allez-vous?",
                        "source_language": "English",
                        "target_language": "French",
                        "request_id": "c4e3f2b1-2345-6789-bcde-f01234567890",
                    }
                }
            },
        },
        422: {"description": "Validation error — missing or invalid fields."},
        500: {"description": "Internal server error from the AI model."},
    },
)
async def translate_endpoint(body: TranslateRequest, request: Request) -> TranslateResponse:
    """
    Translate text into any target language using Google Gemini.

    - **text**: The content to translate (1–5,000 characters).
    - **target_language**: Language to translate into (e.g., 'French', 'Hindi').
    - **source_language**: Source language (default: auto-detect).
    """
    request_id: str = getattr(request.state, "request_id", "unknown")
    return await translate_text(body, request_id)