from rest_framework import serializers

class OnboardingOptionsSerializer(serializers.Serializer):
    motivations = serializers.ListField(required=False)
    daily_goals = serializers.ListField(required=False)
    learning_domains = serializers.ListField(required=False)

class OnboardingOptionsOutputSerializer(serializers.Serializer):
    motivations = serializers.ListField()
    daily_goals = serializers.ListField()
    learning_domains = serializers.ListField()