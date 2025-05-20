from django.utils.translation import gettext_lazy as _
from jsonschema import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from users.models.LearningDomain import LearningDomain
from users.models.LearningMotivation import LearningMotivation
from users.models.LearningPeriodTarget import LearningPeriodTarget
from users.models.UserProfile import UserProfile

User = get_user_model()

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid registration request',
            value={
                'email': 'user@example.com',
                'password': 'securepass123',
                'confirm_password': 'securepass123',
                'full_name': 'John Doe',
                'age': 25,
                'interests': [1, 3, 5],  # IDs of learning domains
                'motivation': 2,         # ID of learning motivation
                'daily_goal': 3          # ID of learning period target
            },
            description='A complete user registration request with profile information'
        )
    ],
    many=False
)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        min_length=8, 
        help_text=_('Password must be at least 8 characters long'),
        error_messages={
            'min_length': _('Password must be at least 8 characters long')
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        help_text=_('Must match the password exactly')
    )
    full_name = serializers.CharField(
        max_length=100,
        help_text=_('User\'s full name')
    )
    age = serializers.IntegerField(
        help_text=_('User\'s age')
    )
    interests = serializers.PrimaryKeyRelatedField(
        queryset=LearningDomain.objects.all(), 
        many=True,
        help_text=_('List of learning domain IDs the user is interested in')
    )
    motivation = serializers.PrimaryKeyRelatedField(
        queryset=LearningMotivation.objects.all(),
        help_text=_('ID of the selected learning motivation')
    )
    daily_goal = serializers.PrimaryKeyRelatedField(
        queryset=LearningPeriodTarget.objects.all(),
        help_text=_('ID of the selected daily learning goal')
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password', 'full_name', 'age', 'interests', 'motivation', 'daily_goal']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {
                'help_text': _('A valid, unique email address'),
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
            raise ValidationError(_("Passwords do not match"))
        
        return attrs
    
    def create(self, validated_data):
        try:
            # Extract profile data
            interests = validated_data.pop('interests')
            motivation = validated_data.pop('motivation')
            daily_goal = validated_data.pop('daily_goal')
            full_name = validated_data.pop('full_name')
            age = validated_data.pop('age')
            
            # Create user
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                is_active=True,
                is_verified=False,
            )
            
            # Create user profile
            from users.models.UserProfile import UserProfile
            profile = UserProfile.objects.create(
                user=user,
                full_name=full_name,
                age=age,
                motivation=motivation,
                daily_goal=daily_goal
            )
            profile.interests.set(interests)
            
            return user
        except Exception as e:
            # Raise a simple string error
            raise ValidationError(str(e))
            
    def to_representation(self, instance):
        """
        Customize the response to include basic profile information
        """
        representation = {
            'id': str(instance.id),
            'email': instance.email,
        }
        
        # Add profile data if available
        if hasattr(instance, 'profile'):
            profile = instance.profile
            representation['full_name'] = profile.full_name
            representation['age'] = profile.age
            representation['interests'] = [interest.id for interest in profile.interests.all()]
            representation['motivation'] = profile.motivation.id if profile.motivation else None
            representation['daily_goal'] = profile.daily_goal.id if profile.daily_goal else None
        
        return representation
