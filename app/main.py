"""
Main FastAPI application entry point.
Registers middleware, exception handlers, and all route modules.
"""

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.logger import get_logger
from app.routes import summarize, translate, generate_email

settings = get_settings()
logger = get_logger(__name__)


# ── Lifespan ───────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Environment: %s | Model: %s", settings.APP_ENV, settings.GEMINI_MODEL)
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


# ── App Instance ───────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "A production-ready REST API built with FastAPI and Google Gemini AI.\n\n"
        "## Endpoints\n"
        "- **POST /summarize** — Summarize any block of text using AI\n"
        "- **POST /translate** — Translate text into any language using AI\n"
        "- **POST /generate-email** — Generate a professional email from a context description\n\n"
        "## Features\n"
        "- Request validation with Pydantic v2\n"
        "- Structured error responses\n"
        "- Request ID tracing\n"
        "- Centralized logging\n"
        "- CORS support\n"
    ),
    contact={
        "name": "Nitin Chauhan",
        "email": "your_email@example.com",
    },
    lifespan=lifespan,
)


# ── Middleware ─────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_and_logging_middleware(request: Request, call_next):
    """
    Middleware that:
    1. Generates a UUID request_id and attaches it to request.state.
    2. Logs the incoming request with method, path, and timestamp.
    3. Logs the outgoing response with status code and execution time.
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()

    logger.info(
        "REQUEST  | id=%s | %s %s",
        request_id,
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "RESPONSE | id=%s | status=%d | duration=%.2fms",
        request_id,
        response.status_code,
        duration_ms,
    )

    response.headers["X-Request-ID"] = request_id
    return response


# ── Exception Handlers ─────────────────────────────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with a structured response."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning("[%s] Validation error: %s", request_id, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Request validation failed. Please check your input.",
            "detail": str(exc.errors()),
            "request_id": request_id,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions with a structured response."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning("[%s] HTTP %d: %s", request_id, exc.status_code, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "detail": None,
            "request_id": request_id,
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueErrors raised from service layer."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error("[%s] ValueError: %s", request_id, str(exc))
    return JSONResponse(
        status_code=400,
        content={
            "error": True,
            "message": str(exc),
            "detail": None,
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all handler for unexpected errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("[%s] Unhandled exception: %s", request_id, str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "An unexpected internal server error occurred.",
            "detail": str(exc),
            "request_id": request_id,
        },
    )


# ── Health Check ───────────────────────────────────────────────────────────────

@app.get(
    "/",
    summary="Health Check",
    description="Returns application name, version, and health status.",
    tags=["Health"],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "app": "IR INFOTECH API Assignment",
                        "version": "1.0.0",
                        "status": "healthy",
                    }
                }
            }
        }
    },
)
async def health_check():
    """Health check endpoint — confirms the service is running."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
    }


# ── Routers ────────────────────────────────────────────────────────────────────

app.include_router(summarize.router)
app.include_router(translate.router)
app.include_router(generate_email.router)