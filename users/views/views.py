from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from core.models import AppConfig
from core.response import APIResponse
from core.serializers.AppConfigSerializer import AppConfigSerializer
from ..serializers.OTPSerializer import OTPSerializer
from ..serializers.OTPVerificationSerializer import OTPVerificationSerializer
from ..serializers.PasswordResetSerializer import PasswordResetSerializer
from ..serializers.LearningDomainSerializer import LearningDomainSerializer
from ..serializers.UserProfileSerializer import UserProfileSerializer
from ..serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from users.serializers import OnboardingOptionsSerializer
from ..models import UserProfile, LearningDomain

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

class OnboardingOptionsView(APIView):
    # permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Prepare options for dropdowns
        discovery_sources = [
            {'value': choice[0], 'label': str(choice[1])} 
            for choice in UserProfile.DISCOVERY_SOURCES
        ]
        
        stem_levels = [
            {'value': choice[0], 'label': str(choice[1])} 
            for choice in UserProfile.STEM_LEVEL_CHOICES
        ]
        
        motivations = [
            {'value': choice[0], 'label': str(choice[1])} 
            for choice in UserProfile.MOTIVATION_CHOICES
        ]
        
        daily_goals = [
            {'value': choice[0], 'label': str(choice[1])} 
            for choice in UserProfile.DAILY_GOAL_CHOICES
        ]
        
        learning_domains = LearningDomain.objects.all()
        learning_domains_serializer = LearningDomainSerializer(learning_domains, many=True, context={'request': request})
        
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
            'primary_color': primary_color.safe_translation_getter('value', any_language=True) if primary_color else '#12D18E',
            'platform_name': platform_name.safe_translation_getter('value', any_language=True) if platform_name else 'SteamUp'
        }
        
        return APIResponse(data=data)