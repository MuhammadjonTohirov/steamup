from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from .response import api_response

def format_error_dict(error_dict):
    """
    Formats a nested error dictionary into a flat string
    
    Example:
    {"password": ["Too short", "Too simple"], "email": ["Invalid format"]}
    becomes:
    "password: Too short. password: Too simple. email: Invalid format."
    """
    if not isinstance(error_dict, dict):
        return str(error_dict)
    
    error_messages = []
    
    for field, errors in error_dict.items():
        if isinstance(errors, list):
            for error in errors:
                if isinstance(error, dict):  # Handle nested dictionaries
                    nested_errors = format_error_dict(error)
                    error_messages.append(f"{field}: {nested_errors}")
                else:
                    error_messages.append(f"{field}: {error}")
        elif isinstance(errors, dict):  # Handle nested dictionaries
            nested_errors = format_error_dict(errors)
            error_messages.append(f"{field}: {nested_errors}")
        else:
            error_messages.append(f"{field}: {errors}")
    
    return ". ".join(error_messages)

def convert_exception_to_string(exc):
    """
    Convert any exception type to a string error message.
    """
    # Handle Django validation errors
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            return format_error_dict(exc.message_dict)
        elif hasattr(exc, 'messages'):
            return ". ".join(exc.messages)
        else:
            return str(exc)
    
    # Handle DRF validation errors
    elif isinstance(exc, DRFValidationError):
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                return format_error_dict(exc.detail)
            elif isinstance(exc.detail, list):
                return ". ".join(str(item) for item in exc.detail)
            else:
                return str(exc.detail)
        else:
            return str(exc)
    
    # Handle generic exceptions
    else:
        return str(exc)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that formats the response according
    to our standardized format with a simple string error message.
    """
    # If it's a Django validation error, convert it to a DRF validation error
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=convert_exception_to_string(exc))
    
    # Call REST framework's default exception handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # Get the status code
        code = response.status_code
        
        # Format the error as a string
        error = convert_exception_to_string(exc)
        
        # Create standardized response
        return Response(
            data=api_response(data=None, error=error, code=code),
            status=code
        )
    else:
        # For uncaught exceptions, return a 500 error
        error = convert_exception_to_string(exc)
        return Response(
            data=api_response(
                data=None, 
                error=error, 
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )