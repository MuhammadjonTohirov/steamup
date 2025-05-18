from django.utils import translation
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware that sets the language based on the Accept-Language header in API requests.
    This middleware should run after Django's LocaleMiddleware but before any processing.
    """
    def process_request(self, request):
        # Check if this is an API request
        if request.path.startswith('/api/'):
            # First check for an explicit language parameter
            lang_param = request.GET.get('lang')
            
            if lang_param and lang_param in [lang[0] for lang in settings.LANGUAGES]:
                # Set the language from query parameter
                translation.activate(lang_param)
                request.LANGUAGE_CODE = lang_param
                logger.debug(f"Language set from query parameter: {lang_param}")
                return None
                
            # Then check the Accept-Language header
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if accept_language:
                # Parse the Accept-Language header to get the preferred language
                languages = [lang.split(';')[0].strip() for lang in accept_language.split(',')]
                # Find the first language that is supported by our application
                for language in languages:
                    language = language.split('-')[0]  # Remove country code if present (e.g., en-US -> en)
                    if language in [lang[0] for lang in settings.LANGUAGES]:
                        # Set the language for this request
                        translation.activate(language)
                        request.LANGUAGE_CODE = language
                        logger.debug(f"Language set from Accept-Language header: {language}")
                        break
            else:
                # Default to settings.LANGUAGE_CODE if no header is present
                lang = settings.LANGUAGE_CODE
                translation.activate(lang)
                request.LANGUAGE_CODE = lang
                logger.debug(f"Language set to default: {lang}")
                    
        return None
        
    def process_response(self, request, response):
        # Add a header to inform which language was used
        if hasattr(request, 'LANGUAGE_CODE'):
            response['Content-Language'] = request.LANGUAGE_CODE
        return response