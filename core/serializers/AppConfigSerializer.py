from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from core.models import AppConfig

class AppConfigSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=AppConfig)
    
    class Meta:
        model = AppConfig
        fields = ['key', 'translations']