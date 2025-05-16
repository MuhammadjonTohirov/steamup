from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from core.response import APIResponse
from .models import OTPCode, UserProfile, LearningDomain, AppConfig
from core.token_views import CustomTokenObtainPairView
from .serializers import (
    UserRegistrationSerializer, CustomTokenObtainPairSerializer,
    OTPSerializer, OTPVerificationSerializer, PasswordResetSerializer,
    UserProfileSerializer, LearningDomainSerializer, OnboardingOptionsSerializer,
    AppConfigSerializer
)

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    throttle_classes = [AnonRateThrottle]
    
    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT token
            token_serializer = CustomTokenObtainPairSerializer(data={
                'email': request.data['email'],
                'password': request.data['password']
            })
            token_serializer.is_valid(raise_exception=True)
            
            return APIResponse(
                data={
                    'user': serializer.data,
                    'token': token_serializer.validated_data
                },
                code=status.HTTP_201_CREATED
            )
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=OTPSerializer,
        responses={200: {'message': 'string'}}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def request_otp(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.save()
            
            # Send email with OTP
            purpose_text = "email verification" if otp.purpose == "verify" else "password reset"
            email_subject = f"SteamUp - Your OTP for {purpose_text}"
            email_body = f"""
            Hello,
            
            Your one-time password (OTP) for {purpose_text} is: {otp.code}
            
            This OTP will expire in 5 minutes.
            
            Best regards,
            The SteamUp Team
            """
            
            try:
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [otp.user.email]
                )
                email.send()
                return APIResponse(data={"message": f"OTP sent to {otp.user.email}"})
            except Exception as e:
                return APIResponse(error=str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    
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
                return APIResponse(data={"message": "Email verified successfully."})
            else:
                return APIResponse(data={"message": "OTP verified successfully."})
        
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
            return APIResponse(data={"message": "Password reset successfully."})
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

class OnboardingOptionsView(APIView):
    # permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Prepare options for dropdowns
        discovery_sources = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in UserProfile.DISCOVERY_CHOICES
        ]
        
        stem_levels = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in UserProfile.STEM_LEVEL_CHOICES
        ]
        
        motivations = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in UserProfile.MOTIVATION_CHOICES
        ]
        
        daily_goals = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in UserProfile.DAILY_GOAL_CHOICES
        ]
        
        learning_domains = LearningDomain.objects.all()
        learning_domains_serializer = LearningDomainSerializer(learning_domains, many=True)
        
        data = {
            'discovery_sources': discovery_sources,
            'stem_levels': stem_levels,
            'motivations': motivations,
            'daily_goals': daily_goals,
            'learning_domains': learning_domains_serializer.data
        }
        
        serializer = OnboardingOptionsSerializer(data)
        return APIResponse(data=serializer.data)

class AppConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def theme(self, request):
        # Get primary color and platform name
        primary_color = AppConfig.objects.filter(key='primary_color').first()
        platform_name = AppConfig.objects.filter(key='platform_name').first()
        
        data = {
            'primary_color': primary_color.value if primary_color else '#12D18E',
            'platform_name': platform_name.value if platform_name else 'SteamUp'
        }
        
        return APIResponse(data=data)