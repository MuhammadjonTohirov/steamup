# swagger_debug.py
# Save this file to the root of your project and run it with:
# python swagger_debug.py

import os
import sys
import django
import traceback

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamup_platform.settings')
django.setup()

from django.urls import get_resolver
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.plumbing import load_docstring_component
from drf_spectacular.validation import validate_schema
from rest_framework import serializers
from rest_framework.views import APIView

def debug_swagger():
    print("Starting Swagger schema debug...")
    
    try:
        # Try to generate the schema
        generator = SchemaGenerator()
        schema = generator.get_schema()
        
        print("Schema generated successfully!")
        
        # Try to validate the schema
        try:
            validate_schema(schema)
            print("Schema validation successful!")
        except Exception as val_error:
            print("Schema validation failed:")
            print(traceback.format_exc())
    
    except Exception as e:
        print("Schema generation failed:")
        print(traceback.format_exc())
        
        # Try to find the problematic endpoint or serializer
        try:
            print("\nAttempting to identify problematic endpoints...")
            
            # Get all URL patterns
            resolver = get_resolver()
            
            # Check each endpoint individually
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'callback') and hasattr(pattern.callback, 'cls'):
                    view_cls = pattern.callback.cls
                    
                    # Skip admin views
                    if pattern.pattern.regex.pattern.startswith('^admin/'):
                        continue
                    
                    # Check if this is an API view
                    if issubclass(view_cls, APIView):
                        url_pattern = pattern.pattern.regex.pattern
                        view_name = view_cls.__name__
                        
                        print(f"Testing endpoint: {url_pattern} ({view_name})")
                        
                        try:
                            # Try to generate schema for just this view
                            mini_generator = SchemaGenerator(patterns=[pattern])
                            mini_schema = mini_generator.get_schema()
                            print(f"  ✓ Schema generation successful for {url_pattern}")
                        except Exception as view_error:
                            print(f"  ✗ Error in endpoint {url_pattern}:")
                            print(f"    {str(view_error)}")
                            
                            # Check serializers used by this view
                            for attr_name in dir(view_cls):
                                attr = getattr(view_cls, attr_name)
                                if isinstance(attr, type) and issubclass(attr, serializers.Serializer):
                                    print(f"    - Uses serializer: {attr.__name__}")
        
        except Exception as debug_error:
            print("Error during debug process:")
            print(traceback.format_exc())
    
    print("\nDebug process complete.")

if __name__ == "__main__":
    debug_swagger()