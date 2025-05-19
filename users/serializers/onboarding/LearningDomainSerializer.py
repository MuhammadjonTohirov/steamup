from users.models.LearningDomain import LearningDomain
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class LearningDomainSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=LearningDomain)
    
    class Meta:
        model = LearningDomain
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
            simplified_translations[lang] = trans.get('name_translated', '')
        
        # remove 'translations' from the representation
        representation.pop('translations', None)
        
        # Add the name field with current language translation
        current_language = self.context.get('language', 'en')
        representation['title'] = simplified_translations.get(current_language, '')
                
        return representation