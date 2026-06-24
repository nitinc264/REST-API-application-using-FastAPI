"""
Centralized Google Gemini API client.
All endpoints share this single reusable service to interact with Gemini.
"""

import google.generativeai as genai
from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class GeminiClient:
    """
    Wrapper around the Google Generative AI SDK.
    Initializes once and provides a simple generate() method.
    """

    def __init__(self) -> None:
        """Configure the Gemini SDK with the API key from settings."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)
        logger.info("GeminiClient initialized with model: %s", settings.GEMINI_MODEL)

    async def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the text response.

        Args:
            prompt: The full prompt string to send to the model.

        Returns:
            The model's text response as a string.

        Raises:
            ValueError: If the model returns an empty or invalid response.
            Exception: Propagates any SDK-level errors.
        """
        logger.debug("Sending prompt to Gemini (length=%d chars)", len(prompt))
        response = self.model.generate_content(prompt)

        if not response or not response.text:
            logger.error("Gemini returned an empty response for prompt: %.100s...", prompt)
            raise ValueError("Gemini returned an empty response. Please try again.")

        logger.debug("Gemini response received (length=%d chars)", len(response.text))
        return response.text.strip()


# Module-level singleton — imported by all service modules
gemini_client = GeminiClient()