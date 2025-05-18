from django.utils.translation import gettext_lazy as _
from jsonschema import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, error_messages={
        'min_length': _('Password must be at least 8 characters long')
    })
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'unique': _('A user with this email already exists'),
                    'invalid': _('Enter a valid email address')
                }
            }
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', '')
        
        if password != confirm_password:
            # Use a simple string instead of a dictionary
            raise ValidationError(_("Passwords do not match"))
        
        return attrs
    
    def create(self, validated_data):
        try:
            # Create a new user with the validated data
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                is_active=True,
                is_verified=False,
            )
            return user
        except Exception as e:
            # Raise a simple string error
            raise DRFValidationError(str(e))