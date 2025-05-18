from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views.token_views import CustomTokenObtainPairView, CustomTokenRefreshView
from users.views import LanguageView

from users.views.AppConfigViewSet import AppConfigViewSet
from users.views.OnboardingOptionsView import OnboardingOptionsView
from users.views.views import (
    AuthViewSet, UserProfileViewSet
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
    path('auth/register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/request-otp/', AuthViewSet.as_view({'post': 'request_otp'}), name='request_otp'),
    path('auth/verify-otp/', AuthViewSet.as_view({'post': 'verify_otp'}), name='verify_otp'),
    path('auth/forgot-password/', AuthViewSet.as_view({'post': 'forgot_password'}), name='forgot_password'),
    path('auth/verify-reset-otp/', AuthViewSet.as_view({'post': 'verify_reset_otp'}), name='verify_reset_otp'),
    path('auth/reset-password/', AuthViewSet.as_view({'post': 'reset_password'}), name='reset_password'),
    
    # Onboarding options
    path('onboarding/options/', OnboardingOptionsView.as_view(), name='onboarding_options'),
    
    # Language settings
    # path('language/', LanguageView.as_view(), name='language'),

]