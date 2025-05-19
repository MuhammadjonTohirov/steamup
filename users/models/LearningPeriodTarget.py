from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class LearningPeriodTarget(TranslatableModel):
    PERIOD_CHOICES = [
        ('daily', _('Day')),
        ('weekly', _('Week')),
        ('monthly', _('Month')),
        ('yearly', _('Year')),
    ]
    
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)
    repeat_count = models.IntegerField(_('Period Value'), default=1)
    period_unit = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='daily', verbose_name=_('Period Unit')) 
    complement = models.CharField(max_length=100, null=True, help_text=_('Great, Awesome, etc'), blank=True)

    translations = TranslatedFields(
        tr_complement=models.CharField(_("Translated complement"), max_length=100, null=True, blank=True), 
    )

    def __str__(self):
        translated_complement = self.safe_translation_getter('tr_complement', any_language=True)
        translated_complement = translated_complement or f"{self.repeat_count} {self.get_period_unit_display()}"
        
        return translated_complement or self.complement or _('Unnamed Target')
    
    def get_period_unit_display(self):
        return dict(self.PERIOD_CHOICES).get(self.period_unit, self.period_unit)