from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status

from core.response import APIResponse

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView that returns a standardized response format
    """
    def post(self, request, *args, **kwargs):
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