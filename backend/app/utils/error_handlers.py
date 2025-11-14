"""
Error Handlers
Sanitized error responses to prevent information leakage
"""

import logging
import uuid
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all unhandled exceptions with sanitized error messages

    Logs full error details internally but returns generic message to user
    to prevent information leakage about system internals.
    """
    # Generate error ID for tracking
    error_id = str(uuid.uuid4())

    # Log full error internally with traceback
    logger.error(
        f"Error ID {error_id} | Path: {request.url.path} | Error: {str(exc)}",
        exc_info=True,
        extra={
            "error_id": error_id,
            "path": request.url.path,
            "method": request.method,
        }
    )

    # Return sanitized error to user
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "detail": "An internal error occurred. Please try again later.",
            "error_id": error_id  # For support purposes
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors with user-friendly messages

    These are safe to show to users as they relate to input format,
    not system internals.
    """
    error_id = str(uuid.uuid4())

    # Log validation error
    logger.warning(
        f"Validation Error ID {error_id} | Path: {request.url.path} | Errors: {exc.errors()}",
        extra={
            "error_id": error_id,
            "path": request.url.path,
            "validation_errors": exc.errors()
        }
    )

    # Format validation errors in user-friendly way
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "detail": "Invalid request data",
            "errors": errors,
            "error_id": error_id
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions raised by routes

    Only passes through the status code and detail message,
    not any internal system information.
    """
    error_id = str(uuid.uuid4())

    # Log HTTP exception
    logger.info(
        f"HTTP Exception ID {error_id} | Path: {request.url.path} | Status: {exc.status_code} | Detail: {exc.detail}",
        extra={
            "error_id": error_id,
            "path": request.url.path,
            "status_code": exc.status_code,
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "detail": exc.detail,
            "error_id": error_id
        }
    )


def sanitize_error_message(error: Exception) -> str:
    """
    Sanitize error messages to remove sensitive information

    Returns a generic message for most errors, preserving only
    safe user-facing messages.
    """
    error_str = str(error)

    # Check for common patterns that should be hidden
    sensitive_patterns = [
        "/home/",
        "/usr/",
        "/var/",
        "\\Users\\",
        "\\Program Files\\",
        ".py",
        "Traceback",
        "File \"",
        "api_key",
        "password",
        "token",
        "secret"
    ]

    for pattern in sensitive_patterns:
        if pattern.lower() in error_str.lower():
            return "An error occurred while processing your request"

    # If error message is safe, return it
    return error_str
