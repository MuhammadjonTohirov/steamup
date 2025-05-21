"""
Django settings for steamup_platform project.
"""

import os
from datetime import timedelta
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']  # Configure appropriately for production

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'parler',  # Add django-parler for translation
    'parler_rest',  # Add django-parler-rest for REST API support
    
    # Local apps
    'core',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Add LocaleMiddleware
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middlewares.StandardResponseMiddleware.StandardResponseMiddleware',  # Standard response middleware
    'core.middlewares.LanguageMiddleware.LanguageMiddleware',  # Add Language middleware for API requests
]

ROOT_URLCONF = 'steamup_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # Add i18n context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'steamup_platform.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'core.validations.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'core.validations.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'core.validations.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'core.validations.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en'  # Default language
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True  # Localized formatting of numbers and dates
USE_TZ = True

# Define available languages
LANGUAGES = [
    ('en', _('English')),
    ('uz', _('Uzbek')),
    ('ru', _('Russian')),
]

# Django Parler settings
PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'uz'},
        {'code': 'ru'},
    ),
    'default': {
        'fallbacks': ['en'],  # Fallback to English if translation not available
        'hide_untranslated': False,  # Show default language if translation not available
    }
}

# Locale paths for storing translation files
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'core.schema.StandardResponseAutoSchema',
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # In production, specify exact origins
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Language']  # Expose Content-Language header

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'UPDATE_LAST_LOGIN': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Email configuration
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('smtp.gmail.com')
    EMAIL_PORT = config('587', cast=int)
    EMAIL_HOST_USER = config('tokhirov.mukhammadjon@gmail.com')
    EMAIL_HOST_PASSWORD = config('jdwn yotq wgal hnjo')
    EMAIL_USE_TLS = config('True', cast=bool)

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'SteamUp API',
    'DESCRIPTION': 'API for SteamUp Platform',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Add these settings for better schema generation
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    # Exclude problematic serializers or views if needed
    'EXCLUDE_PATH_REGEX': [],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # In production, specify exact origins
CORS_ALLOW_CREDENTIALS = True

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'UPDATE_LAST_LOGIN': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Email configuration
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('smtp.gmail.com')
    EMAIL_PORT = config('587', cast=int)
    EMAIL_HOST_USER = config('tokhirov.mukhammadjon@gmail.com')
    EMAIL_HOST_PASSWORD = config('jdwn yotq wgal hnjo')
    EMAIL_USE_TLS = config('True', cast=bool)

# API Documentation
SPECTACULAR_SETTINGS = {
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
    
    'APPEND_COMPONENTS': {
        "schemas": {
            "StandardResponse": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "nullable": True},
                    "error": {"type": "string", "nullable": True},
                    "code": {"type": "integer"}
                },
                "required": ["code"]
            }
        }
    },
    
    'DEFAULT_RESPONSE_CLASS': 'core.schema.StandardResponseSerializer',
}

