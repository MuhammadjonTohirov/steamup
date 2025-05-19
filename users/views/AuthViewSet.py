# users/views/auth/RegisterView.py
from email.message import EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core.response import APIResponse
from core.utils.get_email_templates import get_email_templates
from users.serializers.UserRegistrationSerializer import UserRegistrationSerializer
from users.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from users.serializers.OTPSerializer import OTPSerializer
from users.serializers.OTPVerificationSerializer import OTPVerificationSerializer
from users.serializers.PasswordResetSerializer import PasswordResetSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description="Register a new user",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                response=UserRegistrationSerializer,
                description="User successfully registered"
            ),
            400: OpenApiResponse(
                description="Validation error"
            )
        },
        tags=['auth']
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
                    'token': token_serializer.validated_data
                },
                code=status.HTTP_201_CREATED
            )
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    
class OTPRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=OTPSerializer,
        responses={200: {'message': 'string'}}
    )
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.save()
            
            # Get email templates with translations
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
        
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=OTPVerificationSerializer,
        responses={200: {'message': 'string'}}
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
    
    @extend_schema(
        request={"application/json": {"email": "string", "code": "string"}},
        responses={200: {'message': 'string'}}
    )
    def post(self, request):
        # Add reset purpose to request data
        request.data['purpose'] = 'reset'
        # Delegate to OTPVerificationView
        return OTPVerificationView().post(request)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request={"application/json": {"email": "string"}},
        responses={200: {'message': 'string'}}
    )
    def post(self, request):
        # Add reset purpose to request data
        request.data['purpose'] = 'reset'
        # Delegate to OTPRequestView
        return OTPRequestView().post(request)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=PasswordResetSerializer,
        responses={200: {'message': 'string'}}
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(data={"message": _("Password reset successfully.")})
        return APIResponse(error=serializer.errors, code=status.HTTP_400_BAD_REQUEST)