from modeltranslation.translator import register, TranslationOptions
from users.models.LearningDomain import LearningDomain

@register(LearningDomain)
class LearningDomainTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
