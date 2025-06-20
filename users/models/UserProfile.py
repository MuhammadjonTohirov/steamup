from users.models.LearningDomain import LearningDomain
from users.models.User import User


from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(_('Full Name'), max_length=100)
    age = models.IntegerField(_('Age'))
    interests = models.ManyToManyField(LearningDomain, related_name='users')
    motivation = models.ForeignKey(
        'users.LearningMotivation', related_name='user_motivation', on_delete=models.CASCADE, null=True, blank=True
    )
    daily_goal = models.ForeignKey(
        'users.LearningPeriodTarget', related_name='user_daily_goal', on_delete=models.CASCADE, null=True, blank=True
    )
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"