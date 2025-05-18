# swagger_fix.py
# Save this file to your project root and run:
# python swagger_fix.py

import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamup_platform.settings')
django.setup()

# Check if drf-spectacular is installed correctly
try:
    import drf_spectacular
    print(f"drf-spectacular version: {drf_spectacular.__version__}")
except ImportError:
    print("drf-spectacular is not installed! Install it with:")
    print("pip install drf-spectacular")
    sys.exit(1)

# Apply fixes
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings

# Fix 1: Check and update SPECTACULAR_SETTINGS in settings.py
from django.conf import settings

# Check if SPECTACULAR_SETTINGS exists
if not hasattr(settings, 'SPECTACULAR_SETTINGS'):
    print("SPECTACULAR_SETTINGS not found in settings.py. Adding it...")
    settings.SPECTACULAR_SETTINGS = {
        'TITLE': 'SteamUp API',
        'DESCRIPTION': 'API for SteamUp Platform',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
        'COMPONENT_SPLIT_REQUEST': True,
        'SCHEMA_PATH_PREFIX': '/api/',
        'SWAGGER_UI_SETTINGS': {
            'deepLinking': True,
            'persistAuthorization': True,
            'displayOperationId': True,
        },
        # Schema generation customization
        'ENUM_NAME_OVERRIDES': {},
        'COMPONENT_SPLIT_PATCH': True,
        'COMPONENT_SPLIT_REQUEST': True,
    }
else:
    # Update existing SPECTACULAR_SETTINGS
    updates = {
        'COMPONENT_SPLIT_REQUEST': True,
        'SCHEMA_PATH_PREFIX': '/api/',
        'SWAGGER_UI_SETTINGS': {
            'deepLinking': True,
            'persistAuthorization': True,
            'displayOperationId': True,
        },
    }
    
    # Add missing settings
    for key, value in updates.items():
        if key not in settings.SPECTACULAR_SETTINGS:
            settings.SPECTACULAR_SETTINGS[key] = value
            print(f"Added {key} to SPECTACULAR_SETTINGS")

# Fix 2: Check for common serializer issues
import inspect
from rest_framework import serializers
from drf_spectacular.extensions import OpenApiSerializerExtension

# Collect serializer classes in the project
serializer_classes = []

def find_serializers_in_module(module):
    for name, obj in inspect.getmembers(module):
        # Check if it's a class and subclass of serializers.Serializer
        if inspect.isclass(obj) and issubclass(obj, serializers.Serializer) and obj != serializers.Serializer:
            serializer_classes.append(obj)
        
        # Check for nested modules
        if inspect.ismodule(obj) and obj.__name__.startswith(module.__name__):
            find_serializers_in_module(obj)

# Import and check main app modules
import users
import core

find_serializers_in_module(users)
find_serializers_in_module(core)

print(f"Found {len(serializer_classes)} serializer classes")

# Check for import issues in CustomTokenObtainPairSerializer
try:
    from users.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
    imports = inspect.getmodule(CustomTokenObtainPairSerializer).__dict__
    
    if 'ValidationError' in imports and 'jsonschema' in imports['ValidationError'].__module__:
        print("Warning: CustomTokenObtainPairSerializer imports ValidationError from jsonschema")
        print("This can cause issues with drf-spectacular. Consider changing to:")
        print("from rest_framework.exceptions import ValidationError")
        
        # Check the actual file path
        file_path = inspect.getfile(CustomTokenObtainPairSerializer)
        print(f"File location: {file_path}")
        
except ImportError:
    print("Could not import CustomTokenObtainPairSerializer")

# Fix 3: Check for circular imports
print("\nChecking for potential circular imports...")

# Track import relationships
import_graph = {}

def analyze_imports(module_name):
    try:
        module = __import__(module_name, fromlist=['*'])
        imports = []
        
        for name, value in inspect.getmembers(module):
            if inspect.ismodule(value) and value.__name__ != module_name:
                imports.append(value.__name__)
        
        import_graph[module_name] = imports
        
        # Recursively check imports
        for imp in imports:
            if imp.startswith('users.') or imp.startswith('core.'):
                if imp not in import_graph:
                    analyze_imports(imp)
    except ImportError:
        pass

# Analyze main modules
analyze_imports('users')
analyze_imports('core')

# Function to detect circular dependencies
def find_cycles(graph):
    visited = set()
    path = []
    cycles = []
    
    def dfs(node):
        if node in path:
            # Found a cycle
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        
        if node in visited:
            return
        
        visited.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        
        path.pop()
    
    for node in graph:
        dfs(node)
    
    return cycles

cycles = find_cycles(import_graph)
if cycles:
    print("Detected potential circular imports:")
    for cycle in cycles:
        print(" -> ".join(cycle))
else:
    print("No circular imports detected in the import graph")

# Fix 4: Generate schema manually to test
print("\nTesting manual schema generation...")

try:
    from drf_spectacular.generators import SchemaGenerator
    generator = SchemaGenerator()
    schema = generator.get_schema()
    print("Schema generated successfully!")
except Exception as e:
    print(f"Error during schema generation: {str(e)}")
    import traceback
    traceback.print_exc()

print("\nAll checks complete. See suggestions above for fixing Swagger documentation issues.")