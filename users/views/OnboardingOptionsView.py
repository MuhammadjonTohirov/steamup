from core.response import APIResponse
from users.models.LearningDomain import LearningDomain
from users.models.LearningMotivation import LearningMotivation
from users.models.LearningPeriodTarget import LearningPeriodTarget
from users.models.UserProfile import UserProfile
from users.serializers.onboarding.LearningMotivationSerializer import LearningMotivationSerializer
from users.serializers.onboarding.LearningPeriodTargetSerializer import LearningPeriodTargetSerializer
from users.serializers.onboarding.OnboardingOptionsSerializer import OnboardingOptionsOutputSerializer, OnboardingOptionsSerializer
from users.serializers.onboarding.LearningDomainSerializer import LearningDomainSerializer
from rest_framework.views import APIView
from django.utils.translation import get_language
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class OnboardingOptionsView(APIView):
    serializer_class = OnboardingOptionsOutputSerializer
    
    @extend_schema(
        description="Get onboarding options with translations",
        parameters=[
            OpenApiParameter(
                name='Accept-Language',
                location=OpenApiParameter.HEADER,
                type=str,
                required=False,
                description='Language code (e.g., "en", "uz", "ru")',
                enum=['en', 'uz', 'ru']
            )
        ],
        responses=OnboardingOptionsOutputSerializer
    )
   
    def get(self, request):
        # Get current language
        current_language = get_language() or 'en'
        
        learning_domains = LearningDomain.objects.all()
        learning_domains_serializer = LearningDomainSerializer(
            learning_domains, 
            many=True, 
            context={'request': request, 'language': current_language}
        )
        
        motivations = LearningMotivation.objects.all()
        motivations_serializer = LearningMotivationSerializer(
            motivations, 
            many=True, 
            context={'request': request, 'language': current_language}
        )
        daily_goals = LearningPeriodTargetSerializer(
            LearningPeriodTarget.objects.all(), 
            many=True, 
            context={'request': request, 'language': current_language}
        ).data
        
        data = {
            'motivations': motivations_serializer.data,
            'daily_goals': daily_goals,
            'learning_domains': learning_domains_serializer.data
        }
        
        serializer = OnboardingOptionsSerializer(data)
        return APIResponse(data=serializer.data)
    
    def get_discovery_source(self, choice, request):
        """
        Get discovery sources with translations.
        """
        return {'id': choice[0], 'title': choice[1], 'icon': 'google_icon.png'}