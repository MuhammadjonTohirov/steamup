from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin

from users.app_models.UserProfile import UserProfile

from users.app_models.LearningDomain import LearningDomain

from users.app_models.User import User

from users.app_models.OTPCode import OTPCode

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_verified', 'is_staff', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'purpose', 'is_used', 'created_at')
    list_filter = ('purpose', 'is_used')
    search_fields = ('user__email',)
    ordering = ('-created_at',)

@admin.register(LearningDomain)
class LearningDomainAdmin(TranslatableAdmin):
    list_display = ('name', 'name_translated')    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'age', 'stem_level', 'motivation', 'daily_goal')
    list_filter = ('stem_level', 'motivation', 'daily_goal')
    search_fields = ('user__email', 'full_name')
    filter_horizontal = ('interests',)
    
    