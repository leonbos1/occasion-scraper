"""
API Response Helpers
Standardized response formatting with envelope pattern for consistent error handling.
"""
from typing import Any, Dict, Optional
from flask import jsonify


# Standardized error codes
class ErrorCodes:
    """Centralized error code definitions"""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    AUTH_ERROR = "AUTH_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def success_response(data: Any, metadata: Optional[Dict] = None) -> tuple:
    """
    Create a successful API response with envelope pattern.
    
    Args:
        data: The response data to return
        metadata: Optional metadata to include (pagination, etc.)
    
    Returns:
        Tuple of (response_dict, status_code)
    
    Example:
        return success_response({"cars": [...]}, {"total": 100})
    """
    response = {
        "success": True,
        "data": data
    }
    if metadata:
        response["metadata"] = metadata
    return jsonify(response), 200


def error_response(code: str, message: str, status_code: int = 400, details: Optional[Dict] = None) -> tuple:
    """
    Create an error API response with envelope pattern.
    
    Args:
        code: Standardized error code (use ErrorCodes constants)
        message: User-friendly error message
        status_code: HTTP status code (default 400)
        details: Optional additional error details (field errors, etc.)
    
    Returns:
        Tuple of (response_dict, status_code)
    
    Example:
        return error_response(ErrorCodes.VALIDATION_ERROR, "Invalid input", 400, {"field": "email"})
    """
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        response["error"]["details"] = details
    return jsonify(response), status_code


def validation_error(message: str, details: Optional[Dict] = None) -> tuple:
    """Convenience function for validation errors"""
    return error_response(ErrorCodes.VALIDATION_ERROR, message, 400, details)


def not_found_error(message: str = "Resource not found") -> tuple:
    """Convenience function for not found errors"""
    return error_response(ErrorCodes.NOT_FOUND, message, 404)


def auth_error(message: str = "Authentication failed") -> tuple:
    """Convenience function for authentication errors"""
    return error_response(ErrorCodes.AUTH_ERROR, message, 401)


def database_error(message: str = "Database operation failed", include_details: bool = False, details: Optional[Dict] = None) -> tuple:
    """
    Convenience function for database errors.
    
    Args:
        message: User-friendly error message
        include_details: Whether to include technical details (only in development)
        details: Optional error details
    """
    # In production, hide technical details
    if not include_details:
        details = None
    return error_response(ErrorCodes.DATABASE_ERROR, message, 500, details)
