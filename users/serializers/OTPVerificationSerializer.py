from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from jsonschema import ValidationError
from rest_framework import serializers
from datetime import timedelta

from users.models.OTPCode import OTPCode
from django.contrib.auth import get_user_model

User = get_user_model()

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=OTPCode.PURPOSE_CHOICES)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        purpose = attrs.get('purpose')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User with this email does not exist."))

        # Check for valid OTP
        otp = OTPCode.objects.filter(
            user=user,
            code=code,
            purpose=purpose,
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()

        if not otp:
            raise Exception(_("Invalid or expired OTP code."))
        elif otp.is_used:
            raise Exception(_("This OTP code has already been used."))
        elif otp.purpose != purpose:
            raise Exception(_("This OTP code is not valid for the requested purpose."))

        attrs['user'] = user
        attrs['otp'] = otp
        return attrs