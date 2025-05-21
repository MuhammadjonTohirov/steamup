# users/views/auth/RegisterView.py
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core.response import APIResponse
from core.schema import get_standard_response_schema
from core.utils.get_email_templates import get_email_templates
from core.utils.swagger_helper import api_schema
from users.serializers.HasProfileSerializer import HasProfileSerializer
from users.serializers.UserRegistrationSerializer import UserRegistrationSerializer
from users.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from users.serializers.OTPSerializer import OTPSerializer
from users.serializers.OTPVerificationSerializer import OTPVerificationSerializer
from users.serializers.PasswordResetSerializer import PasswordResetSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @api_schema(
        description="Register a new user",
        request=UserRegistrationSerializer,
        status_code=201,
        success_data={
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "age": 25,
                "interests": [1, 3, 5],
                "motivation": 2,
                "daily_goal": 3
            },
            "creds": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "is_verified": False
            }
        },
        tags=["auth"]
    )
    def post(self, request):
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
                    'creds': token_serializer.validated_data
                },
                code=status.HTTP_201_CREATED
            )
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    
class OTPRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @api_schema(
        request=OTPSerializer,
        success_data={
            "message": "OTP sent to user@example.com"
        },
        tags=["auth"],
    )
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.save()
            purpose = otp.purpose
            email_subject, email_body = get_email_templates(purpose, otp.code)
            
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
        
        return APIResponse(error='User not found', code=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @api_schema(
        request=OTPVerificationSerializer,
        success_data={
            "message": "OTP verified successfully"
        },
        tags=["auth"],
    )
    def post(self, request):
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

class VerifyResetOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @api_schema(
        request=OTPVerificationSerializer,
        success_data={"email": "string", "code": "string"},
        tags=["auth"],
    )
    def post(self, request):
        # Add reset purpose to request data
        request.data['purpose'] = 'reset'
        # Delegate to OTPVerificationView
        return OTPVerificationView().post(request)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @api_schema(
        request=OTPSerializer,
        success_data={"email": "string"},
        tags=["auth"],
    )
    def post(self, request):
        # Add reset purpose to request data
        request.data['purpose'] = 'reset'
        # Delegate to OTPRequestView
        return OTPRequestView().post(request)

# method to check profile exists or not
class HasProfileView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @api_schema(
        request=HasProfileSerializer,
        success_data={"exists": "boolean"},
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return APIResponse(error="Email is required", code=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if not user:
            return APIResponse(data={"exists": False})
        
        return APIResponse(data={"exists": True})

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @api_schema(
        request=PasswordResetSerializer,
        success_data={'message': 'string'}
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(data={"message": _("Password reset successfully.")})
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)