from users.app_models.LearningDomain import LearningDomain
from users.app_models.User import User


from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    # Discovery sources - make translatable
    DISCOVERY_SOURCES = [
        ('google', _('Google')),
        ('facebook', _('Facebook')),
        ('tiktok', _('TikTok')),
        ('playstore', _('Play Store')),
        ('tv', _('TV')),
    ]

    # STEM levels - make translatable
    STEM_LEVEL_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    ]

    # Daily goals - make translatable
    DAILY_GOAL_CHOICES = [
        (5, _('5 minutes')),
        (10, _('10 minutes')),
        (15, _('15 minutes')),
        (30, _('30 minutes')),
        (60, _('60 minutes')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(_('Full Name'), max_length=100)
    age = models.IntegerField(_('Age'))
    interests = models.ManyToManyField(LearningDomain, related_name='users')
    discovery_source = models.CharField(_('Discovery Source'), max_length=20, choices=DISCOVERY_SOURCES)
    stem_level = models.CharField(_('STEM Level'), max_length=20, choices=STEM_LEVEL_CHOICES)
    motivation = models.OneToOneField(
        'users.LearningMotivation', related_name='user_motivation', on_delete=models.CASCADE, null=True, blank=True
    )
    daily_goal = models.IntegerField(_('Daily Goal'), choices=DAILY_GOAL_CHOICES)

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"