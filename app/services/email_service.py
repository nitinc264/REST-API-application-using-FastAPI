"""
Business logic for the /generate-email endpoint.
Constructs the Gemini prompt and parses subject + body from the response.
"""

from app.services.gemini_client import gemini_client
from app.models.schemas import GenerateEmailRequest, GenerateEmailResponse
from app.logger import get_logger

logger = get_logger(__name__)


async def generate_email(request: GenerateEmailRequest, request_id: str) -> GenerateEmailResponse:
    """
    Generate a professional email subject and body using the Gemini API.

    Args:
        request: Validated GenerateEmailRequest with context, tone, and optional names.
        request_id: Unique identifier for this request (for logging/tracing).

    Returns:
        GenerateEmailResponse with subject, body, and tone.

    Raises:
        ValueError: If response cannot be parsed into subject and body.
    """
    recipient_line = f"Recipient name: {request.recipient_name}" if request.recipient_name else ""
    sender_line = f"Sender name: {request.sender_name}" if request.sender_name else ""
    tone = request.tone or "professional"

    logger.info("[%s] Generating email (tone=%s)", request_id, tone)

    prompt = (
        f"You are a professional email writing assistant.\n"
        f"Write a complete email based on the following details:\n"
        f"Context: {request.context}\n"
        f"Tone: {tone}\n"
        f"{recipient_line}\n"
        f"{sender_line}\n\n"
        f"You MUST format your response exactly as follows — no extra text before or after:\n"
        f"SUBJECT: <email subject here>\n"
        f"BODY:\n<full email body here>"
    )

    raw_response = await gemini_client.generate(prompt)

    subject, body = _parse_email_response(raw_response, request_id)

    logger.info("[%s] Email generated successfully (tone=%s)", request_id, tone)

    return GenerateEmailResponse(
        subject=subject,
        body=body,
        tone=tone,
        request_id=request_id,
    )


def _parse_email_response(raw: str, request_id: str) -> tuple[str, str]:
    """
    Parse the Gemini response into subject and body components.

    Args:
        raw: Raw text returned by Gemini.
        request_id: For logging context.

    Returns:
        A tuple of (subject, body).

    Raises:
        ValueError: If the expected SUBJECT:/BODY: markers are not found.
    """
    subject = ""
    body = ""

    lines = raw.strip().splitlines()

    for i, line in enumerate(lines):
        if line.upper().startswith("SUBJECT:"):
            subject = line[len("SUBJECT:"):].strip()
        elif line.upper().startswith("BODY:"):
            body = "\n".join(lines[i + 1:]).strip()
            break

    if not subject or not body:
        logger.warning(
            "[%s] Could not parse SUBJECT/BODY markers from Gemini response. "
            "Falling back to heuristic split.",
            request_id,
        )
        # Fallback: treat first line as subject, rest as body
        parts = raw.strip().split("\n", 1)
        subject = parts[0].strip()
        body = parts[1].strip() if len(parts) > 1 else raw.strip()

    if not subject:
        raise ValueError("Gemini did not return a valid email subject. Please try again.")
    if not body:
        raise ValueError("Gemini did not return a valid email body. Please try again.")

    return subject, body