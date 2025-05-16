from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator as DjangoUserAttributeSimilarityValidator,
    MinimumLengthValidator as DjangoMinimumLengthValidator,
    CommonPasswordValidator as DjangoCommonPasswordValidator,
    NumericPasswordValidator as DjangoNumericPasswordValidator
)

class UserAttributeSimilarityValidator(DjangoUserAttributeSimilarityValidator):
    """
    Custom validator that returns string errors instead of dictionaries.
    """
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError as e:
            # Convert the error to a simple string
            raise ValidationError(
                _("Password is too similar to your personal information."),
                code='password_too_similar',
            )

class MinimumLengthValidator(DjangoMinimumLengthValidator):
    """
    Custom validator that returns string errors instead of dictionaries.
    """
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError as e:
            # Convert the error to a simple string
            raise ValidationError(
                _("Password must be at least %(min_length)d characters long.") % {'min_length': self.min_length},
                code='password_too_short',
            )

class CommonPasswordValidator(DjangoCommonPasswordValidator):
    """
    Custom validator that returns string errors instead of dictionaries.
    """
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError as e:
            # Convert the error to a simple string
            raise ValidationError(
                _("This password is too common and easily guessed."),
                code='password_too_common',
            )

class NumericPasswordValidator(DjangoNumericPasswordValidator):
    """
    Custom validator that returns string errors instead of dictionaries.
    """
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError as e:
            # Convert the error to a simple string
            raise ValidationError(
                _("Password cannot be entirely numeric."),
                code='password_entirely_numeric',
            )