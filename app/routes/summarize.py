"""
Route handler for POST /summarize.
Thin handler — all logic lives in summarize_service.
"""

from fastapi import APIRouter, Request
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.summarize_service import summarize_text

router = APIRouter()


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    summary="Summarize Text",
    description=(
        "Accepts a block of text and returns a concise AI-generated summary. "
        "You can optionally specify a `max_length` (in words) to control how brief the summary is. "
        "Powered by Google Gemini."
    ),
    response_description="A JSON object containing the summary and word count metadata.",
    tags=["NLP"],
    responses={
        200: {
            "description": "Summary generated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "AI is revolutionizing industries by enabling faster decisions and personalized experiences.",
                        "original_length": 52,
                        "summary_length": 14,
                        "request_id": "b3d2f1a0-1234-5678-abcd-ef0123456789",
                    }
                }
            },
        },
        422: {"description": "Validation error — missing or invalid fields."},
        500: {"description": "Internal server error from the AI model."},
    },
)
async def summarize_endpoint(body: SummarizeRequest, request: Request) -> SummarizeResponse:
    """
    Summarize the provided text using Google Gemini.

    - **text**: The content to summarize (20–10,000 characters).
    - **max_length**: Target summary length in words (default: 150).
    """
    request_id: str = getattr(request.state, "request_id", "unknown")
    return await summarize_text(body, request_id)