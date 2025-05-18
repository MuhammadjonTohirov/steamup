from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from .models.OTPCode import OTPCode

from .models.UserProfile import UserProfile

from .models.LearningDomain import LearningDomain

from .models.AppConfig import AppConfig

from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from .models.AppConfig import AppConfig

User = get_user_model()

class AuthTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.request_otp_url = reverse('request_otp')
        self.verify_otp_url = reverse('verify_otp')
        self.forgot_password_url = reverse('forgot_password')
        self.verify_reset_otp_url = reverse('verify_reset_otp')
        self.reset_password_url = reverse('reset_password')
        
        # Create a verified user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            is_verified=True
        )
        
        # Create an unverified user for testing
        self.unverified_user = User.objects.create_user(
            email='unverified@example.com',
            password='testpassword123',
            is_verified=False
        )
    
    def test_user_registration(self):
        """Test user registration with valid data"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # 2 from setUp + 1 new
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
    
    def test_user_registration_password_mismatch(self):
        """Test user registration with mismatched passwords"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirm_password': 'differentpassword'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)
    
    def test_user_login(self):
        """Test user login with valid credentials"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['is_verified'], True)
    
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_request_otp_for_verification(self):
        """Test requesting OTP for email verification"""
        data = {
            'email': 'unverified@example.com',
            'purpose': 'verify'
        }
        
        response = self.client.post(self.request_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Check if OTP was created
        otp_exists = OTPCode.objects.filter(
            user=self.unverified_user,
            purpose='verify',
            is_used=False
        ).exists()
        self.assertTrue(otp_exists)
    
    def test_verify_otp(self):
        """Test verifying OTP for email verification"""
        # Create an OTP for the unverified user
        otp = OTPCode.objects.create(
            user=self.unverified_user,
            code='123456',
            purpose='verify',
            is_used=False
        )
        
        data = {
            'email': 'unverified@example.com',
            'code': '123456',
            'purpose': 'verify'
        }
        
        response = self.client.post(self.verify_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh user from database
        self.unverified_user.refresh_from_db()
        self.assertTrue(self.unverified_user.is_verified)
        
        # Check if OTP was marked as used
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)
    
    def test_verify_otp_invalid_code(self):
        """Test verifying OTP with invalid code"""
        # Create an OTP for the unverified user
        OTPCode.objects.create(
            user=self.unverified_user,
            code='123456',
            purpose='verify',
            is_used=False
        )
        
        data = {
            'email': 'unverified@example.com',
            'code': '654321',  # Wrong code
            'purpose': 'verify'
        }
        
        response = self.client.post(self.verify_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Refresh user from database
        self.unverified_user.refresh_from_db()
        self.assertFalse(self.unverified_user.is_verified)
    
    def test_forgot_password(self):
        """Test forgot password flow"""
        data = {
            'email': 'test@example.com',
            'purpose': 'reset'
        }
        
        response = self.client.post(self.forgot_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if OTP was created
        otp_exists = OTPCode.objects.filter(
            user=self.user,
            purpose='reset',
            is_used=False
        ).exists()
        self.assertTrue(otp_exists)
    
    def test_verify_reset_otp(self):
        """Test verifying OTP for password reset"""
        # Create an OTP for the user
        otp = OTPCode.objects.create(
            user=self.user,
            code='654321',
            purpose='reset',
            is_used=False
        )
        
        data = {
            'email': 'test@example.com',
            'code': '654321',
            'purpose': 'reset'
        }
        
        response = self.client.post(self.verify_reset_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if OTP was marked as used
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)
    
    def test_reset_password(self):
        """Test resetting password"""
        # Create an OTP for the user
        OTPCode.objects.create(
            user=self.user,
            code='654321',
            purpose='reset',
            is_used=False
        )
        
        data = {
            'email': 'test@example.com',
            'code': '654321',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        
        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if user can login with new password
        login_data = {
            'email': 'test@example.com',
            'password': 'newpassword123'
        }
        
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
    
    def test_otp_throttling(self):
        """Test OTP throttling (cannot request OTP within 60 seconds)"""
        # First request
        data = {
            'email': 'test@example.com',
            'purpose': 'verify'
        }
        
        response = self.client.post(self.request_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Second request within 60 seconds
        response = self.client.post(self.request_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('throttled', response.data)
    
    def test_otp_expiration(self):
        """Test OTP expiration (OTP expires after 5 minutes)"""
        # Create an expired OTP
        expired_otp = OTPCode.objects.create(
            user=self.user,
            code='111111',
            purpose='verify',
            is_used=False,
            created_at=timezone.now() - timedelta(minutes=6)  # 6 minutes old
        )
        
        data = {
            'email': 'test@example.com',
            'code': '111111',
            'purpose': 'verify'
        }
        
        response = self.client.post(self.verify_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('code', response.data)

class UserProfileTestCase(APITestCase):
    def setUp(self):
        self.profile_url = reverse('profile-list')
        self.onboarding_options_url = reverse('onboarding_options')
        
        # Create a user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            is_verified=True
        )
        
        # Create learning domains
        self.domain1 = LearningDomain.objects.create(name='Physics')
        self.domain2 = LearningDomain.objects.create(name='Chemistry')
        self.domain3 = LearningDomain.objects.create(name='Biology')
        
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
    
    def test_create_profile(self):
        """Test creating a user profile"""
        data = {
            'full_name': 'Test User',
            'age': 25,
            'interests': [self.domain1.id, self.domain3.id],
            'discovery_source': 'google',
            'stem_level': 'intermediate',
            'motivation': 'career',
            'daily_goal': 30
        }
        
        response = self.client.post(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if profile was created correctly
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.full_name, 'Test User')
        self.assertEqual(profile.age, 25)
        self.assertEqual(profile.discovery_source, 'google')
        self.assertEqual(profile.stem_level, 'intermediate')
        self.assertEqual(profile.motivation, 'career')
        self.assertEqual(profile.daily_goal, 30)
        self.assertEqual(list(profile.interests.all()), [self.domain1, self.domain3])
    
    def test_update_profile(self):
        """Test updating an existing user profile"""
        # Create a profile first
        profile = UserProfile.objects.create(
            user=self.user,
            full_name='Test User',
            age=25,
            discovery_source='google',
            stem_level='beginner',
            motivation='fun',
            daily_goal=5
        )
        profile.interests.add(self.domain1)
        
        # Update the profile
        data = {
            'full_name': 'Updated Name',
            'age': 30,
            'interests': [self.domain2.id, self.domain3.id],
            'discovery_source': 'facebook',
            'stem_level': 'advanced',
            'motivation': 'growth',
            'daily_goal': 60
        }
        
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if profile was updated correctly
        profile.refresh_from_db()
        self.assertEqual(profile.full_name, 'Updated Name')
        self.assertEqual(profile.age, 30)
        self.assertEqual(profile.discovery_source, 'facebook')
        self.assertEqual(profile.stem_level, 'advanced')
        self.assertEqual(profile.motivation, 'growth')
        self.assertEqual(profile.daily_goal, 60)
        self.assertEqual(list(profile.interests.all()), [self.domain2, self.domain3])
    
    def test_get_profile(self):
        """Test retrieving a user profile"""
        # Create a profile
        profile = UserProfile.objects.create(
            user=self.user,
            full_name='Test User',
            age=25,
            discovery_source='google',
            stem_level='beginner',
            motivation='fun',
            daily_goal=5
        )
        profile.interests.add(self.domain1)
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Test User')
        self.assertEqual(response.data['age'], 25)
        self.assertEqual(response.data['discovery_source'], 'google')
        self.assertEqual(response.data['stem_level'], 'beginner')
        self.assertEqual(response.data['motivation'], 'fun')
        self.assertEqual(response.data['daily_goal'], 5)
        self.assertEqual(len(response.data['interests']), 1)
        self.assertEqual(response.data['interests'][0], self.domain1.id)
    
    def test_get_onboarding_options(self):
        """Test retrieving onboarding options"""
        response = self.client.get(self.onboarding_options_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if all option categories are present
        self.assertIn('discovery_sources', response.data)
        self.assertIn('stem_levels', response.data)
        self.assertIn('motivations', response.data)
        self.assertIn('daily_goals', response.data)
        self.assertIn('learning_domains', response.data)
        
        # Check if learning domains are correct
        domains = response.data['learning_domains']
        self.assertEqual(len(domains), 3)
        domain_names = [domain['name'] for domain in domains]
        self.assertIn('Physics', domain_names)
        self.assertIn('Chemistry', domain_names)
        self.assertIn('Biology', domain_names)

class AppConfigTestCase(APITestCase):
    def setUp(self):
        self.config_theme_url = reverse('config-theme')
        
        # Create app config entries
        AppConfig.objects.create(key='primary_color', value='#12D18E')
        AppConfig.objects.create(key='platform_name', value='SteamUp')
    
    def test_get_theme_config(self):
        """Test retrieving theme configuration"""
        response = self.client.get(self.config_theme_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if theme config is correct
        self.assertEqual(response.data['primary_color'], '#12D18E')
        self.assertEqual(response.data['platform_name'], 'SteamUp')