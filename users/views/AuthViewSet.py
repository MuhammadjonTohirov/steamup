from core.response import APIResponse
from users.serializers import UserRegistrationSerializer
from users.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from users.serializers.OTPSerializer import OTPSerializer
from users.serializers.OTPVerificationSerializer import OTPVerificationSerializer
from users.serializers.PasswordResetSerializer import PasswordResetSerializer

from rest_framework.throttling import AnonRateThrottle
from django.utils.translation import gettext as _, gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from core.response import APIResponse


class AuthViewSet(viewsets.GenericViewSet):
    throttle_classes = [AnonRateThrottle]
    
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
        methods=['POST'],
        tags=['Authentication']
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