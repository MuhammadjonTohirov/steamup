# Step 1: Transitional model with both original and translated fields
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class AppConfig(TranslatableModel):
    # Keep the original field temporarily during migration
    value = models.CharField(max_length=255, null=True)
    key = models.CharField(_('Key'), max_length=50, unique=True)

    # Add translated fields with different names to avoid conflicts
    translations = TranslatedFields(
        value_translated=models.CharField(_('Value'), max_length=255)
    )

    def __str__(self):
        translated_value = self.safe_translation_getter('value_translated', any_language=True)
        return f"{self.key}: {translated_value or self.value or ''}"
   
   
class Image(models.Model):
    custom_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Image for {self.custom_key}"
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None