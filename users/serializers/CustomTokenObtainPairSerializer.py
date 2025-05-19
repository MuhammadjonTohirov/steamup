from jsonschema import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from datetime import timedelta


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        # Remove remember_me from attrs to avoid validation error
        remember_me = attrs.pop('remember_me', False)

        try:
            data = super().validate(attrs)

            # Check if user is verified
            user = self.user
            if not user.is_verified:
                raise ValidationError(_("Email not verified. Please verify your email before logging in."))
                
            # Add custom claims
            data['user_id'] = str(user.id)
            data['email'] = user.email
            data['is_verified'] = user.is_verified

            # Adjust token lifetime based on remember_me flag
            if remember_me:
                refresh = self.get_token(user)
                refresh.set_exp(lifetime=timedelta(days=30))
                data['refresh'] = str(refresh)

            return data
        except Exception as e:
            # Convert any exception to a simple string error
            raise ValidationError(str(e))