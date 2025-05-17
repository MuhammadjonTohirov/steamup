#!/usr/bin/env python

"""
This script populates translation tables for existing data.
Run this after migrating to the translatable models.
"""

import os
import sys
import django

# Add the project path to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamup_platform.settings')
django.setup()

from django.utils import translation
from users.models import LearningDomain, AppConfig

def setup_learning_domain_translations():
    """
    Set up translations for existing LearningDomain records.
    """
    print("Setting up LearningDomain translations...")
    
    # English translations (already exist)
    for domain in LearningDomain.objects.all():
        print(f"Processing domain: {domain.pk}")
        
        # Get the original name
        english_name = domain.safe_translation_getter('name', language_code='en')
        
        if not english_name:
            # If no English translation exists, try to get the name from any language
            english_name = domain.safe_translation_getter('name', any_language=True)
            
            if english_name:
                # Set the English translation
                translation.activate('en')
                domain.set_current_language('en')
                domain.name = english_name
                domain.save()
                print(f"  - Set English translation: {english_name}")
            else:
                # No name found at all, this is an error
                print(f"  - ERROR: No name found for domain {domain.pk}")
                continue
        
        # Set Uzbek translation
        translation.activate('uz')
        domain.set_current_language('uz')
        
        # Map English names to Uzbek translations
        uz_translations = {
            'Physics': 'Fizika',
            'Chemistry': 'Kimyo',
            'Biology': 'Biologiya',
            'Mathematics': 'Matematika',
            'Computer Science': 'Kompyuter Fanlari',
            'Engineering': 'Muhandislik',
            'Robotics': 'Robotlashuv',
            'Astronomy': 'Astronomiya',
            'Environmental Science': 'Atrof-muhit Fanlari',
        }
        
        domain.name = uz_translations.get(english_name, english_name)
        domain.save()
        print(f"  - Set Uzbek translation: {domain.name}")
        
        # Set Russian translation
        translation.activate('ru')
        domain.set_current_language('ru')
        
        # Map English names to Russian translations
        ru_translations = {
            'Physics': 'Физика',
            'Chemistry': 'Химия',
            'Biology': 'Биология',
            'Mathematics': 'Математика',
            'Computer Science': 'Информатика',
            'Engineering': 'Инженерия',
            'Robotics': 'Робототехника',
            'Astronomy': 'Астрономия',
            'Environmental Science': 'Экология',
        }
        
        domain.name = ru_translations.get(english_name, english_name)
        domain.save()
        print(f"  - Set Russian translation: {domain.name}")

def setup_app_config_translations():
    """
    Set up translations for existing AppConfig records.
    """
    print("\nSetting up AppConfig translations...")
    
    # English translations (already exist)
    for config in AppConfig.objects.all():
        print(f"Processing config: {config.key}")
        
        # Get the original value
        english_value = config.safe_translation_getter('value', language_code='en')
        
        if not english_value:
            # If no English translation exists, try to get the value from any language
            english_value = config.safe_translation_getter('value', any_language=True)
            
            if english_value:
                # Set the English translation
                translation.activate('en')
                config.set_current_language('en')
                config.value = english_value
                config.save()
                print(f"  - Set English translation: {english_value}")
            else:
                # No value found at all, this is an error
                print(f"  - ERROR: No value found for config {config.key}")
                continue
        
        # For platform_name, set translations
        if config.key == 'platform_name':
            # Set Uzbek translation
            translation.activate('uz')
            config.set_current_language('uz')
            config.value = "SteamUp"
            config.save()
            print(f"  - Set Uzbek translation: {config.value}")
            
            # Set Russian translation
            translation.activate('ru')
            config.set_current_language('ru')
            config.value = "SteamUp"
            config.save()
            print(f"  - Set Russian translation: {config.value}")
        else:
            # For other configs like primary_color, just copy the English value
            translation.activate('uz')
            config.set_current_language('uz')
            config.value = english_value
            config.save()
            print(f"  - Set Uzbek translation: {config.value}")
            
            translation.activate('ru')
            config.set_current_language('ru')
            config.value = english_value
            config.save()
            print(f"  - Set Russian translation: {config.value}")

if __name__ == '__main__':
    # Reset to default language
    translation.activate('en')
    
    # Set up translations
    setup_learning_domain_translations()
    setup_app_config_translations()
    
    print("\nTranslation setup complete!")