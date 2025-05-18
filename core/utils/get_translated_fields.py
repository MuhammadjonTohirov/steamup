from django.utils import translation
from django.conf import settings

def get_translated_field(obj, field_name, language=None, default_language=None):
    """
    Get a translated field value from a translatable model.
    
    Args:
        obj: The translatable model instance
        field_name: The name of the field to get
        language: The language code to get the translation for (defaults to current active language)
        default_language: The language code to use if the translation is not available (defaults to settings.LANGUAGE_CODE)
    
    Returns:
        The translated value or None if not found
    """
    if not language:
        language = translation.get_language()
    
    if not default_language:
        default_language = settings.LANGUAGE_CODE
    
    # Try to get the translation in the requested language
    try:
        obj.set_current_language(language)
        return getattr(obj, field_name)
    except (AttributeError, ValueError):
        # If no translation exists in the requested language, try the default language
        try:
            obj.set_current_language(default_language)
            return getattr(obj, field_name)
        except (AttributeError, ValueError):
            # If still no translation, use any available translation
            try:
                return obj.safe_translation_getter(field_name, any_language=True)
            except (AttributeError, ValueError):
                return None