from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

class BaseAPISerializer(serializers.Serializer):
    """
    Base serializer that overrides the validation behavior to ensure 
    all validation errors are simple strings rather than dictionaries.
    
    Extend this instead of serializers.Serializer or serializers.ModelSerializer
    to get consistent string error messages.
    """
    def is_valid(self, raise_exception=False):
        """
        Override default is_valid to catch and format validation errors
        """
        try:
            return super().is_valid(raise_exception=raise_exception)
        except DRFValidationError as exc:
            self._formatted_errors = self._format_errors(exc.detail)
            if raise_exception:
                raise DRFValidationError(self._formatted_errors)
            return False
    
    def _format_errors(self, errors):
        """
        Convert error dictionary/list to a simple string
        """
        if isinstance(errors, dict):
            # Format dictionary of errors
            formatted = []
            for field, error_list in errors.items():
                if isinstance(error_list, list):
                    for error in error_list:
                        if isinstance(error, dict):
                            # Handle nested errors
                            nested = self._format_errors(error)
                            formatted.append(f"{field}: {nested}")
                        else:
                            formatted.append(f"{field}: {error}")
                elif isinstance(error_list, dict):
                    # Handle nested errors
                    nested = self._format_errors(error_list)
                    formatted.append(f"{field}: {nested}")
                else:
                    formatted.append(f"{field}: {error_list}")
            return ". ".join(formatted)
        elif isinstance(errors, list):
            # Format list of errors
            return ". ".join(str(error) for error in errors)
        else:
            # Return string version of error
            return str(errors)

class BaseModelSerializer(serializers.ModelSerializer, BaseAPISerializer):
    """
    Base model serializer with string error formatting
    """
    pass

# Example usage:
"""
class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
"""