from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class LearningDomain(TranslatableModel):
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)
    title = models.CharField(max_length=100, null=True)

    translations = TranslatedFields(
        name_translated=models.CharField(_("Translated name"), max_length=100, null=True, blank=True), 
    )

    def __str__(self):
        translated_name = self.safe_translation_getter('name_translated', any_language=True)
        return translated_name or self.title or _('Unnamed Domain')