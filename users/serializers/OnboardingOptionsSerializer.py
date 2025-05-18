from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class OnboardingOptionsSerializer(serializers.Serializer):
    discovery_sources = serializers.ListField()
    stem_levels = serializers.ListField()
    motivations = serializers.ListField()
    daily_goals = serializers.ListField()
    learning_domains = serializers.ListField()

    class Meta:
        fields = [
            'discovery_sources',
            'stem_levels',
            'motivations',
            'daily_goals',
            'learning_domains'
        ]
        
    

class OnboardingOptionsOutputSerializer(serializers.Serializer):
    discovery_sources = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    stem_levels = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    motivations = serializers.ListField()
    daily_goals = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    learning_domains = serializers.ListField()