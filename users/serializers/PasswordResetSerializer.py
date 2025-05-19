from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from jsonschema import ValidationError
from rest_framework import serializers
from datetime import timedelta

from users.models.OTPCode import OTPCode
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError(_("Passwords do not match."))

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(_("User with this email does not exist."))

        # Check for valid OTP
        otp = OTPCode.objects.filter(
            user=user,
            code=code,
            purpose='reset',
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()

        if not otp:
            raise ValidationError(_("Invalid or expired OTP code."))

        attrs['user'] = user
        attrs['otp'] = otp
        return attrs

    def save(self):
        user = self.validated_data['user']
        otp = self.validated_data['otp']

        # Update password
        user.set_password(self.validated_data['new_password'])
        user.save()

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        return user