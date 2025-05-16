from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
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
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
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

class LearningDomain(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    DISCOVERY_CHOICES = [
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('playstore', 'Play Store'),
        ('tv', 'TV'),
    ]
    
    STEM_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    MOTIVATION_CHOICES = [
        ('fun', 'Fun'),
        ('career', 'Career'),
        ('education', 'Education'),
        ('growth', 'Growth'),
        ('society', 'Society'),
    ]
    
    DAILY_GOAL_CHOICES = [
        (5, '5 minutes'),
        (10, '10 minutes'),
        (15, '15 minutes'),
        (30, '30 minutes'),
        (60, '60 minutes'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    interests = models.ManyToManyField(LearningDomain, related_name='users')
    discovery_source = models.CharField(max_length=20, choices=DISCOVERY_CHOICES)
    stem_level = models.CharField(max_length=20, choices=STEM_LEVEL_CHOICES)
    motivation = models.CharField(max_length=20, choices=MOTIVATION_CHOICES)
    daily_goal = models.IntegerField(choices=DAILY_GOAL_CHOICES)
    
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"

class OTPCode(models.Model):
    PURPOSE_CHOICES = [
        ('verify', 'Verify'),
        ('reset', 'Reset'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"OTP for {self.user.email} ({self.purpose})"
    
    class Meta:
        ordering = ['-created_at']

class AppConfig(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.key}: {self.value}"