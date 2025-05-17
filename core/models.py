from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AppConfig(TranslatableModel):
    translations = TranslatedFields(
        value=models.CharField(_('Value'), max_length=255)
    )
    key = models.CharField(_('Key'), max_length=50, unique=True)
    
    def __str__(self):
        value = self.safe_translation_getter('value', any_language=True)
        return f"{self.key}: {value}"