from users.models.LearningPeriodTarget import LearningPeriodTarget
from users.models.LearningDomain import LearningDomain
from users.models.LearningMotivation import LearningMotivation
from users.models.UserProfile import UserProfile


from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=LearningDomain.objects.all(), many=True)
    motivation = serializers.PrimaryKeyRelatedField(queryset=LearningMotivation.objects.all(), many=False)
    daily_goal = serializers.PrimaryKeyRelatedField(queryset=LearningPeriodTarget.objects.all(), many=False)
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'age', 'interests', 'motivation', 'daily_goal'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        interests = validated_data.pop('interests')
        motivation = validated_data.pop('motivation', None)
        daily_goal = validated_data.pop('daily_goal', None)
        user = self.context['request'].user

        # Create profile
        profile = UserProfile.objects.create(user=user, **validated_data)

        # Add interests
        profile.interests.set(interests)
        profile.motivation.set(motivation)
        profile.daily_goal.set(daily_goal)
        return profile

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', None)
        motivation = validated_data.pop('motivation', None)
        
        # Update other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Update interests if provided
        if interests is not None:
            instance.interests.set(interests)
            
        if motivation is not None:
            instance.motivation.set(motivation)

        instance.save()
        return instance