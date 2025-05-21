from jsonschema import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _  

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
                
            # Add custom claims
            data['user_id'] = str(user.id)
            data['email'] = user.email
            data['is_verified'] = user.is_verified
            
            if not user.is_verified:
                # pop the refresh token if user is not verified
                data.pop('refresh', None)
                data.pop('access', None)

            # Adjust token lifetime based on remember_me flag
            if remember_me and user.is_verified:
                refresh = self.get_token(user)
                refresh.set_exp(lifetime=timedelta(days=30))
                data['refresh'] = str(refresh)

            return data
        except Exception as e:
            # Convert any exception to a simple string error
            raise Exception(str(e))