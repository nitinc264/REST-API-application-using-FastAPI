"""
Unit and integration tests for the POST /summarize endpoint.
Uses FastAPI TestClient with a mocked Gemini client.
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MOCK_SUMMARY = "AI is transforming industries with faster decisions and better predictions."
SAMPLE_TEXT = (
    "Artificial intelligence is transforming industries across the globe. "
    "From healthcare to finance, AI-powered tools are enabling faster decisions, "
    "better predictions, and more personalized user experiences at scale."
)


@pytest.fixture(autouse=True)
def mock_gemini():
    """Patch GeminiClient.generate for all tests in this module."""
    with patch(
        "app.services.summarize_service.gemini_client.generate",
        new_callable=AsyncMock,
        return_value=MOCK_SUMMARY,
    ):
        yield


class TestSummarizeSuccess:
    """Tests for successful /summarize requests."""

    def test_summarize_returns_200(self):
        """Should return HTTP 200 with a valid text input."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT})
        assert response.status_code == 200

    def test_summarize_response_contains_summary(self):
        """Response should contain a non-empty summary string."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT})
        data = response.json()
        assert "summary" in data
        assert len(data["summary"]) > 0

    def test_summarize_response_contains_word_counts(self):
        """Response should include original_length and summary_length."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT})
        data = response.json()
        assert "original_length" in data
        assert "summary_length" in data
        assert data["original_length"] > 0
        assert data["summary_length"] > 0

    def test_summarize_response_contains_request_id(self):
        """Response should contain a request_id field."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT})
        data = response.json()
        assert "request_id" in data
        assert data["request_id"] is not None

    def test_summarize_with_custom_max_length(self):
        """Should accept a custom max_length parameter."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT, "max_length": 30})
        assert response.status_code == 200

    def test_summarize_response_header_has_request_id(self):
        """Response headers should include X-Request-ID."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT})
        assert "x-request-id" in response.headers


class TestSummarizeValidationErrors:
    """Tests for invalid /summarize input."""

    def test_missing_text_field_returns_422(self):
        """Should return 422 when text field is missing."""
        response = client.post("/summarize", json={})
        assert response.status_code == 422

    def test_text_too_short_returns_422(self):
        """Should return 422 when text is shorter than 20 characters."""
        response = client.post("/summarize", json={"text": "Too short"})
        assert response.status_code == 422

    def test_text_too_long_returns_422(self):
        """Should return 422 when text exceeds 10,000 characters."""
        response = client.post("/summarize", json={"text": "a" * 10001})
        assert response.status_code == 422

    def test_invalid_max_length_too_low_returns_422(self):
        """Should return 422 when max_length is below minimum (30)."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT, "max_length": 5})
        assert response.status_code == 422

    def test_invalid_max_length_too_high_returns_422(self):
        """Should return 422 when max_length exceeds maximum (500)."""
        response = client.post("/summarize", json={"text": SAMPLE_TEXT, "max_length": 999})
        assert response.status_code == 422

    def test_error_response_has_correct_structure(self):
        """422 error response should have error, message, and detail fields."""
        response = client.post("/summarize", json={})
        data = response.json()
        assert data["error"] is True
        assert "message" in data


class TestSummarizeEdgeCases:
    """Edge case tests for /summarize."""

    def test_text_at_minimum_length(self):
        """Should accept text at exactly the minimum length (20 chars)."""
        response = client.post("/summarize", json={"text": "a" * 20})
        assert response.status_code == 200

    def test_text_at_maximum_length(self):
        """Should accept text at exactly the maximum length (10,000 chars)."""
        response = client.post("/summarize", json={"text": "word " * 2000})
        assert response.status_code == 200