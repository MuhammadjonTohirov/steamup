from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from core.response import APIResponse
from ..serializers.OTPSerializer import OTPSerializer
from ..serializers.OTPVerificationSerializer import OTPVerificationSerializer
from ..serializers.PasswordResetSerializer import PasswordResetSerializer
from ..serializers.UserProfileSerializer import UserProfileSerializer
from ..serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from users.app_models.UserProfile import UserProfile

User = get_user_model()

from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from core.response import APIResponse
from core.utils import get_email_templates
from django.core.mail import EmailMessage
from django.conf import settings

from ..serializers.OTPSerializer import OTPSerializer
from ..serializers.OTPVerificationSerializer import OTPVerificationSerializer
from ..serializers.PasswordResetSerializer import PasswordResetSerializer
from ..serializers.UserRegistrationSerializer import UserRegistrationSerializer
from ..serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    
    @extend_schema(
        request=OTPVerificationSerializer,
        responses={200: {'message': 'string'}}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify_otp(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp = serializer.validated_data['otp']
            purpose = serializer.validated_data['purpose']
            
            # Mark OTP as used
            otp.is_used = True
            otp.save()
            
            # If verification purpose, mark user as verified
            if purpose == 'verify':
                user.is_verified = True
                user.save()
                return APIResponse(data={"message": _("Email verified successfully.")})
            else:
                return APIResponse(data={"message": _("OTP verified successfully.")})
        
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=OTPSerializer,
        responses={200: {'message': 'string'}}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def forgot_password(self, request):
        # Reuse the request_otp endpoint with purpose=reset
        request.data['purpose'] = 'reset'
        return self.request_otp(request)
    
    @extend_schema(
        request=OTPVerificationSerializer,
        responses={200: {'message': 'string'}}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def verify_reset_otp(self, request):
        # Reuse the verify_otp endpoint with purpose=reset
        request.data['purpose'] = 'reset'
        return self.verify_otp(request)
    
    @extend_schema(
        request=PasswordResetSerializer,
        responses={200: {'message': 'string'}}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(data={"message": _("Password reset successfully.")})
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'full_name': '',
                'age': 0,
                'discovery_source': 'google',
                'stem_level': 'beginner',
                'motivation': 'fun',
                'daily_goal': 5
            }
        )
        return obj
    
    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse(data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        # If profile already exists, update it
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile, data=request.data)
        except UserProfile.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return APIResponse(data=serializer.data, code=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()

