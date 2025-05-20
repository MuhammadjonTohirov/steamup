from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

from core.response import APIResponse

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView that returns a standardized response format
    """
    def post(self, request, *args, **kwargs):
        # check is user is verified
        # if not, return error
        # if user is verified, return token
        # and user details
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return APIResponse(error="Email is required", code=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return APIResponse(error="User is not verified", code=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return APIResponse(error=str(e), code=status.HTTP_401_UNAUTHORIZED)
        
        return APIResponse(data=serializer.validated_data)

class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom TokenRefreshView that returns a standardized response format
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return APIResponse(error=str(e), code=status.HTTP_401_UNAUTHORIZED)
        
        return APIResponse(data=serializer.validated_data)