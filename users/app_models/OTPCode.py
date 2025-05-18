from users.app_models.User import User


from django.db import models
from django.utils.translation import gettext_lazy as _


class OTPCode(models.Model):
    PURPOSE_CHOICES = [
        ('verify', _('Verify')),
        ('reset', _('Reset')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(_('Code'), max_length=6)
    purpose = models.CharField(_('Purpose'), max_length=10, choices=PURPOSE_CHOICES)
    is_used = models.BooleanField(_('Is Used'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email} ({self.purpose})"

    class Meta:
        ordering = ['-created_at']