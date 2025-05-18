from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class LearningMotivation(TranslatableModel):
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)
    title = models.CharField(max_length=100, null=True)

    translations = TranslatedFields(
        tr_title=models.CharField(_("Translated title"), max_length=100, null=True, blank=True), 
    )

    def __str__(self):
        translated_name = self.safe_translation_getter('tr_title', any_language=True)
        return translated_name or self.title or _('Unnamed Domain')