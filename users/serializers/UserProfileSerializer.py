from users.app_models.LearningDomain import LearningDomain
from users.app_models.UserProfile import UserProfile


from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=LearningDomain.objects.all(), many=True)

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'age', 'interests', 'discovery_source',
            'stem_level', 'motivation', 'daily_goal'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        interests = validated_data.pop('interests')
        user = self.context['request'].user

        # Create profile
        profile = UserProfile.objects.create(user=user, **validated_data)

        # Add interests
        profile.interests.set(interests)

        return profile

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', None)

        # Update other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Update interests if provided
        if interests is not None:
            instance.interests.set(interests)

        instance.save()
        return instance