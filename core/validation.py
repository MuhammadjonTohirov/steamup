from rest_framework.serializers import ValidationError as DRFValidationError

class StringValidationError(DRFValidationError):
    """
    Custom validation error class that ensures errors are always strings.
    Use this instead of the default ValidationError to get consistent string errors.
    """
    def __init__(self, detail):
        # If detail is a dictionary or list, convert it to a string
        if isinstance(detail, dict):
            error_str = "; ".join(f"{k}: {v}" for k, v in detail.items())
            super().__init__(error_str)
        elif isinstance(detail, list):
            error_str = "; ".join(str(item) for item in detail)
            super().__init__(error_str)
        else:
            # If it's already a string or other primitive, use it directly
            super().__init__(detail)

# Example usage in a serializer:
"""
from core.validation import StringValidationError

def validate(self, attrs):
    if not attrs.get('password') == attrs.get('confirm_password'):
        raise StringValidationError("Passwords do not match")
    return attrs
"""