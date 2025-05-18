from users.app_models.LearningMotivation import LearningMotivation
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class LearningMotivationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=LearningMotivation)
    
    class Meta:
        model = LearningMotivation
        fields = ['id', 'icon', 'translations']
        
    def to_representation(self, instance):
        """
        Customize the representation to make it more user-friendly.
        Instead of returning the full translations object, just return
        simplified translations.
        """
        representation = super().to_representation(instance)
        
        # Simplify the translations format
        simplified_translations = {}
        for lang, trans in representation.get('translations', {}).items():
            simplified_translations[lang] = trans.get('tr_title', '')
        
        representation.pop('translations', None)

        # Add the name field with current language translation
        current_language = self.context.get('language', 'en')
        representation['title'] = simplified_translations.get(current_language, '')
                
        return representation