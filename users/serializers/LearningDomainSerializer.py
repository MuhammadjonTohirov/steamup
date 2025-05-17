from users.models import LearningDomain


from rest_framework import serializers


class LearningDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningDomain
        fields = ['id', 'name']