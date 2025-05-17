from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from jsonschema import ValidationError
from rest_framework import serializers
import random
from datetime import timedelta

from users.models import OTPCode
from django.contrib.auth import get_user_model

User = get_user_model()

class OTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = OTPCode
        fields = ['email', 'purpose']

    def validate(self, attrs):
        email = attrs.pop('email')
        purpose = attrs.get('purpose')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if purpose == 'verify':
                raise ValidationError(_("User with this email does not exist."))
            else:
                raise ValidationError(_("User with this email does not exist."))

        # Check for throttling (no OTP within 60 seconds)
        recent_otp = OTPCode.objects.filter(
            user=user,
            purpose=purpose,
            created_at__gte=timezone.now() - timedelta(seconds=60),
            is_used=False
        ).first()

        if recent_otp:
            time_passed = timezone.now() - recent_otp.created_at
            time_left = 60 - time_passed.seconds
            raise ValidationError(
                _("Please wait {seconds} seconds before requesting another OTP.").format(seconds=time_left)
            )

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        purpose = validated_data.get('purpose')

        # Generate a 6-digit OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Create the OTP record
        otp = OTPCode.objects.create(
            user=user,
            code=otp_code,
            purpose=purpose,
            is_used=False
        )

        return otp