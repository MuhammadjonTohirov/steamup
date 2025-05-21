from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class HasProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()

    