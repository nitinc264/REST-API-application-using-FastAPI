"""
Business logic for the /summarize endpoint.
Constructs the Gemini prompt and parses the response.
"""

from app.services.gemini_client import gemini_client
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.logger import get_logger

logger = get_logger(__name__)


async def summarize_text(request: SummarizeRequest, request_id: str) -> SummarizeResponse:
    """
    Summarize the provided text using the Gemini API.

    Args:
        request: Validated SummarizeRequest containing text and max_length.
        request_id: Unique identifier for this request (for logging/tracing).

    Returns:
        SummarizeResponse with the summary and word count metadata.

    Raises:
        ValueError: If Gemini returns an unusable response.
    """
    logger.info("[%s] Summarizing text of %d words", request_id, len(request.text.split()))

    prompt = (
        f"You are a professional summarization assistant.\n"
        f"Summarize the following text in a clear and concise manner.\n"
        f"The summary must be no longer than {request.max_length} words.\n"
        f"Return ONLY the summary text — no headings, no labels, no extra commentary.\n\n"
        f"Text to summarize:\n{request.text}"
    )

    summary = await gemini_client.generate(prompt)

    original_length = len(request.text.split())
    summary_length = len(summary.split())

    logger.info(
        "[%s] Summary generated: %d → %d words",
        request_id,
        original_length,
        summary_length,
    )

    return SummarizeResponse(
        summary=summary,
        original_length=original_length,
        summary_length=summary_length,
        request_id=request_id,
    )