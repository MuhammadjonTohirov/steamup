from django.contrib import admin
from core.models import AppConfig, Image


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)
    
    def get_image_url(self, obj):
        return obj.get_image_url()
    
    get_image_url.short_description = 'Image URL'