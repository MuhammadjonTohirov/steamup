from users.app_models.LearningDomain import LearningDomain
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class LearningDomainSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=LearningDomain)
    
    class Meta:
        model = LearningDomain
        fields = ['id', 'translations']
        
    def to_representation(self, instance):
        """
        Customize the representation to make it more user-friendly.
        Instead of returning the full translations object, just return
        the current translation.
        """
        # Get the standard representation
        representation = super().to_representation(instance)
        
        # Add a simple "name" field with the current translation
        current_translation = representation.get('translations', {}).get(self.context.get('language', 'en'), {})
        if current_translation:
            representation['name'] = current_translation.get('name', '')
        else:
            # Fallback to any available translation
            for lang, trans in representation.get('translations', {}).items():
                if trans.get('name'):
                    representation['name'] = trans.get('name')
                    break
            else:
                representation['name'] = ''
                
        return representation