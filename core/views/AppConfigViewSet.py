from core.models import AppConfig
from core.response import APIResponse
from core.serializers.AppConfigSerializer import AppConfigSerializer
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from django.utils.translation import get_language

class AppConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_context(self):
        """Add current language to serializer context"""
        context = super().get_serializer_context()
        context['language'] = get_language() or 'en'
        return context
    
    @action(detail=False, methods=['get'])
    def theme(self, request):
        # Get current language
        current_language = get_language() or 'en'
        
        # Get primary color and platform name
        primary_color = AppConfig.objects.filter(key='primary_color').first()
        platform_name = AppConfig.objects.filter(key='platform_name').first()
        
        # Get translated values
        if primary_color:
            try:
                primary_color.set_current_language(current_language)
                primary_color_value = primary_color.value
            except:
                primary_color_value = primary_color.safe_translation_getter('value', any_language=True) or '#12D18E'
        else:
            primary_color_value = '#12D18E'
            
        if platform_name:
            try:
                platform_name.set_current_language(current_language)
                platform_name_value = platform_name.value
            except:
                platform_name_value = platform_name.safe_translation_getter('value', any_language=True) or 'SteamUp'
        else:
            platform_name_value = 'SteamUp'
        
        data = {
            'primary_color': primary_color_value,
            'platform_name': platform_name_value
        }
        
        return APIResponse(data=data)
    
from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from parler_rest.serializers import TranslatedFieldsField

class TranslatedFieldsFieldExtension(OpenApiSerializerFieldExtension):
    target_class = TranslatedFieldsField

    def map_serializer_field(self, auto_schema, direction):
        return {
            'type': 'object',
            'additionalProperties': {
                'type': 'object',
                'properties': {
                    'value': {
                        'type': 'string',
                        'description': 'Translated value'
                    }
                }
            }
        }