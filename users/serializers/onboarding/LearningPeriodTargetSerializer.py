from users.app_models.LearningPeriodTarget import LearningPeriodTarget
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from django.utils.translation import gettext_lazy as _

class LearningPeriodTargetSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=LearningPeriodTarget)
    
    class Meta:
        model = LearningPeriodTarget
        fields = ['id', 'period_unit', 'repeat_count', 'complement', 'translations']  # Added 'translations' to fields list
     
    def period_str(self, obj) -> str:
        if obj == 'daily':
            return _('day')
        if obj == 'weekly':
            return _('week')
        if obj == 'monthly':
            return _('month')
        if obj == 'yearly':
            return _('year')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        simplified_translations = {}
        for lang, trans in representation.get('translations', {}).items():
            simplified_translations[lang] = trans.get('tr_complement', '')
        
        representation['translations'] = simplified_translations
        representation.pop('translations', None)  # Remove the original translations field
        current_language = self.context.get('language', 'en')
        
        count = representation.pop('repeat_count', 1)
        period_unit = representation.pop('period_unit', 'daily')
        representation['title'] = f"{count} / {self.period_str(period_unit)}"
        representation['comment'] = simplified_translations.get(current_language, representation.pop('complement', ''))
        representation['icon'] = None
                
        return representation