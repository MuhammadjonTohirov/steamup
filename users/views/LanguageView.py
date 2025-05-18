from django.utils.translation import activate, get_language
from django.utils import translation
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings

from core.response import APIResponse

class LanguageView(APIView):
    """
    API view to get available languages and set the current language.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Get the list of available languages and the current language.
        """
        # Get available languages
        available_languages = [
            {'code': lang_code, 'name': str(lang_name)}
            for lang_code, lang_name in settings.LANGUAGES
        ]
        
        # Get current language
        current_language = get_language()
        
        data = {
            'available_languages': available_languages,
            'current_language': current_language,
        }
        
        return APIResponse(data=data)
    
    def post(self, request):
        """
        Set the current language.
        """
        # Get language code from request data
        language_code = request.data.get('language')
        
        # Check if language code is valid
        if language_code not in [lang[0] for lang in settings.LANGUAGES]:
            return APIResponse(error="Invalid language code", code=400)
        
        # Activate the language
        translation.activate(language_code)
        
        # Set language in the session
        if hasattr(request, 'session'):
            request.session[translation.LANGUAGE_SESSION_KEY] = language_code
        
        # Return success response with new language
        return APIResponse(data={
            'message': "Language changed successfully",
            'language': language_code,
        })