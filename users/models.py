from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

class LearningDomain(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100)
    )
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or _('Unnamed Domain')

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
    
    # Motivations - make translatable
    MOTIVATION_CHOICES = [
        ('fun', _('Fun')),
        ('career', _('Career')),
        ('education', _('Education')),
        ('growth', _('Growth')),
        ('society', _('Society')),
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
    motivation = models.CharField(_('Motivation'), max_length=20, choices=MOTIVATION_CHOICES)
    daily_goal = models.IntegerField(_('Daily Goal'), choices=DAILY_GOAL_CHOICES)
    
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"

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
