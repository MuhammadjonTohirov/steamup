from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views.token_views import CustomTokenObtainPairView, CustomTokenRefreshView
from users.views import LanguageView

from core.views.AppConfigViewSet import AppConfigViewSet
from users.views.AuthViewSet import ForgotPasswordView, HasProfileView, RegisterView, OTPRequestView, OTPVerificationView, PasswordResetView, VerifyResetOTPView
from users.views.OnboardingOptionsView import OnboardingOptionsView
from users.views.UserProfileViewSet import (
    UserProfileViewSet
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'config', AppConfigViewSet, basename='config')

# Create URL patterns
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # Auth ViewSet actions
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/request-otp/', OTPRequestView.as_view(), name='request_otp'),
    path('auth/verify-otp/', OTPVerificationView.as_view(), name='verify_otp'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/verify-reset-otp/', VerifyResetOTPView.as_view(), name='verify_reset_otp'),
    path('auth/reset-password/', PasswordResetView.as_view(), name='reset_password'),
    # auth/has-profile/
    path('auth/has-profile/', HasProfileView.as_view(), name='has_profile'),
    
    # Onboarding options
    path('onboarding/options/', OnboardingOptionsView.as_view(), name='onboarding_options'),
    
    # Language settings
    # path('language/', LanguageView.as_view(), name='language'),

]