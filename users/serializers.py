from jsonschema import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import OTPCode, UserProfile, LearningDomain, AppConfig
import random

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    remember_me = serializers.BooleanField(required=False, default=False)
    
    def validate(self, attrs):
        # Remove remember_me from attrs to avoid validation error
        remember_me = attrs.pop('remember_me', False)
        
        try:
            data = super().validate(attrs)
            
            # Add custom claims
            user = self.user
            data['user_id'] = str(user.id)
            data['email'] = user.email
            data['is_verified'] = user.is_verified
            
            # Adjust token lifetime based on remember_me flag
            if remember_me:
                refresh = self.get_token(user)
                refresh.set_exp(lifetime=timedelta(days=30))
                data['refresh'] = str(refresh)
                
            return data
        except Exception as e:
            # Convert any exception to a simple string error
            raise ValidationError(str(e))

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, error_messages={
        'min_length': 'Password must be at least 8 characters long'
    })
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'unique': 'A user with this email already exists',
                    'invalid': 'Enter a valid email address'
                }
            }
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', '')
        
        if password != confirm_password:
            # Use a simple string instead of a dictionary
            raise ValidationError("Passwords do not match")
        
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

class OTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = OTPCode
        fields = ['email', 'purpose']
    
    
    def validate(self, attrs):
        email = attrs.pop('email')
        purpose = attrs.get('purpose')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if purpose == 'verify':
                raise ValidationError("User with this email does not exist.")
            else:
                raise ValidationError("User with this email does not exist.")
        
        # Check for throttling (no OTP within 60 seconds)
        recent_otp = OTPCode.objects.filter(
            user=user,
            purpose=purpose,
            created_at__gte=timezone.now() - timedelta(seconds=60),
            is_used=False
        ).first()
        
        if recent_otp:
            time_passed = timezone.now() - recent_otp.created_at
            time_left = 60 - time_passed.seconds
            raise ValidationError(
                f"Please wait {time_left} seconds before requesting another OTP."
            )
        
        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        user = validated_data.get('user')
        purpose = validated_data.get('purpose')
        
        # Generate a 6-digit OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Create the OTP record
        otp = OTPCode.objects.create(
            user=user,
            code=otp_code,
            purpose=purpose,
            is_used=False
        )
        
        return otp

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=OTPCode.PURPOSE_CHOICES)
    
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        purpose = attrs.get('purpose')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")
        
        # Check for valid OTP
        otp = OTPCode.objects.filter(
            user=user,
            code=code,
            purpose=purpose,
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()
        
        if not otp:
            raise ValidationError("Invalid or expired OTP code.")
        
        attrs['user'] = user
        attrs['otp'] = otp
        return attrs

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")
        
        # Check for valid OTP
        otp = OTPCode.objects.filter(
            user=user,
            code=code,
            purpose='reset',
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()
        
        if not otp:
            raise ValidationError("Invalid or expired OTP code.")
        
        attrs['user'] = user
        attrs['otp'] = otp
        return attrs
    
    def save(self):
        user = self.validated_data['user']
        otp = self.validated_data['otp']
        
        # Update password
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        # Mark OTP as used
        otp.is_used = True
        otp.save()
        
        return user

class LearningDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningDomain
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=LearningDomain.objects.all(), many=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'age', 'interests', 'discovery_source',
            'stem_level', 'motivation', 'daily_goal'
        ]
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        interests = validated_data.pop('interests')
        user = self.context['request'].user
        
        # Create profile
        profile = UserProfile.objects.create(user=user, **validated_data)
        
        # Add interests
        profile.interests.set(interests)
        
        return profile
    
    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', None)
        
        # Update other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        # Update interests if provided
        if interests is not None:
            instance.interests.set(interests)
        
        instance.save()
        return instance

class OnboardingOptionsSerializer(serializers.Serializer):
    discovery_sources = serializers.ListField(
        child=serializers.DictField()
    )
    stem_levels = serializers.ListField(
        child=serializers.DictField()
    )
    motivations = serializers.ListField(
        child=serializers.DictField()
    )
    daily_goals = serializers.ListField(
        child=serializers.DictField()
    )
    learning_domains = LearningDomainSerializer(many=True)

class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = ['key', 'value']