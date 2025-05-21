from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from drf_spectacular.extensions import OpenApiSerializerExtension
from rest_framework import serializers
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_basic_type

class StandardResponseSerializer(serializers.Serializer):
    """Base serializer for standardized API responses"""
    data = serializers.JSONField(help_text="Response data", allow_null=True)
    error = serializers.CharField(help_text="Error message if any", allow_null=True)
    code = serializers.IntegerField(help_text="HTTP status code")
    
    class Meta:
        ref_name = "StandardResponse"

def get_standard_response_schema(data_schema=None):
    """Generate a response schema with our standard format"""
    class StandardResponseWithData(StandardResponseSerializer):
        data = data_schema() if data_schema else serializers.JSONField(allow_null=True)
        
        class Meta:
            ref_name = None  # Avoid polluting schema with every response variation
    
    return StandardResponseWithData

class StandardResponseAutoSchema(AutoSchema):
    def get_response_schemas(self, response_serializers):
        responses = super().get_response_schemas(response_serializers)
        
        # Wrap each response in our standard format if not already wrapped
        for status_code, response in responses.items():
            content = response.get('content', {})
            for media_type, media_object in content.items():
                schema = media_object.get('schema', {})
                
                # Check if it's already a standard response
                if not (
                    schema.get('type') == 'object' and 
                    'data' in schema.get('properties', {}) and
                    'error' in schema.get('properties', {}) and
                    'code' in schema.get('properties', {})
                ):
                    # Wrap in standard response
                    media_object['schema'] = {
                        'type': 'object',
                        'properties': {
                            'data': schema if schema else build_basic_type({}),
                            'error': {
                                'type': 'string',
                                'nullable': True,
                            },
                            'code': {
                                'type': 'integer',
                                'default': int(status_code),
                            }
                        },
                        'required': ['code']
                    }
        
        return responses
    
    
from drf_spectacular.extensions import OpenApiViewExtension
from core.response import APIResponse

class APIResponseSchemaFixer(OpenApiViewExtension):
    """Extension for fixing APIResponse schema"""
    target_class = 'core.response.APIResponse'
    
    def view_replacement(self):
        from rest_framework.response import Response
        
        class FixedAPIResponse(APIResponse):
            """APIResponse subclass with fixed schema"""
            schema = StandardResponseSerializer().schema
        
        return FixedAPIResponse