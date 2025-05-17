from users.serializers.LearningDomainSerializer import LearningDomainSerializer


from rest_framework import serializers


class OnboardingOptionsSerializer(serializers.Serializer):
    discovery_sources = serializers.ListField(
        child=serializers.DictField()
    )
    stem_levels = serializers.ListField(
        child=serializers.DictField()
    )
    motivations = serializers.ListField(
        child=serializers.DictField()
    )
    daily_goals = serializers.ListField(
        child=serializers.DictField()
    )
    learning_domains = LearningDomainSerializer(many=True)