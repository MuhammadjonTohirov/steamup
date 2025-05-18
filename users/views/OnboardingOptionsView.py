from core.response import APIResponse
from users.app_models.LearningDomain import LearningDomain
from users.app_models.UserProfile import UserProfile
from users.serializers import OnboardingOptionsSerializer
from users.serializers.LearningDomainSerializer import LearningDomainSerializer
from rest_framework.views import APIView
from django.utils.translation import get_language

class OnboardingOptionsView(APIView):
    # permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Get current language
        current_language = get_language() or 'en'
        
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
        learning_domains_serializer = LearningDomainSerializer(
            learning_domains, 
            many=True, 
            context={'request': request, 'language': current_language}
        )
        
        data = {
            'discovery_sources': discovery_sources,
            'stem_levels': stem_levels,
            'motivations': motivations,
            'daily_goals': daily_goals,
            'learning_domains': learning_domains_serializer.data
        }
        
        serializer = OnboardingOptionsSerializer(data)
        return APIResponse(data=serializer.data)