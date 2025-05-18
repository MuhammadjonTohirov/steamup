from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class LearningDomain(TranslatableModel):
    # Keep the original field temporarily during migration
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)
    name = models.CharField(max_length=100, null=True)

    # Add translated fields with different names to avoid conflicts
    translations = TranslatedFields(
        # show as simply name
        name_translated=models.CharField(_("Translated name"), max_length=100, null=True, blank=True), 
    )

    def __str__(self):
        """
        Return a string representation of the LearningDomain instance.
        
        If a translated name is available, it returns that, otherwise it falls 
        back to the original name. If neither is available, it returns 'Unnamed Domain'.
        """

        translated_name = self.safe_translation_getter('name_translated', any_language=True)
        return translated_name or self.name or _('Unnamed Domain')