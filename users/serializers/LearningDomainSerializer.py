from users.models import LearningDomain
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class LearningDomainSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=LearningDomain)
    
    class Meta:
        model = LearningDomain
        fields = ['id', 'translations']