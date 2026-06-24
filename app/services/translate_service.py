"""
Business logic for the /translate endpoint.
Constructs the Gemini prompt and parses the response.
"""

from app.services.gemini_client import gemini_client
from app.models.schemas import TranslateRequest, TranslateResponse
from app.logger import get_logger

logger = get_logger(__name__)


async def translate_text(request: TranslateRequest, request_id: str) -> TranslateResponse:
    """
    Translate the provided text into the target language using the Gemini API.

    Args:
        request: Validated TranslateRequest with text, target_language, source_language.
        request_id: Unique identifier for this request (for logging/tracing).

    Returns:
        TranslateResponse with translated text and language metadata.

    Raises:
        ValueError: If Gemini returns an unusable response.
    """
    source_info = (
        f"The source language is {request.source_language}."
        if request.source_language and request.source_language.lower() != "auto-detect"
        else "Auto-detect the source language."
    )

    logger.info(
        "[%s] Translating to '%s' (source: %s)",
        request_id,
        request.target_language,
        request.source_language,
    )

    prompt = (
        f"You are a professional translation assistant.\n"
        f"{source_info}\n"
        f"Translate the following text accurately into {request.target_language}.\n"
        f"Preserve the original meaning, tone, and formatting.\n"
        f"Return ONLY the translated text — no labels, no explanations.\n\n"
        f"Text to translate:\n{request.text}"
    )

    translated_text = await gemini_client.generate(prompt)

    detected_source = request.source_language or "auto-detect"

    logger.info("[%s] Translation completed to '%s'", request_id, request.target_language)

    return TranslateResponse(
        translated_text=translated_text,
        source_language=detected_source,
        target_language=request.target_language,
        request_id=request_id,
    )