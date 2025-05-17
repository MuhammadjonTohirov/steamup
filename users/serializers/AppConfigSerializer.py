from users.models import AppConfig


from rest_framework import serializers


class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = ['key', 'value']