import pytest
from django.test import TestCase
from .models import UserProfile, CustomUser

# backend/users/test_models.py

class UserProfileModelTest(TestCase):
    def test_calculate_completion_percentage_all_fields(self):
        user = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        user.profile_picture = "test.jpg"
        user.bio = "Test bio"
        user.linkedin_url = "https://linkedin.com"
        user.github_url = "https://github.com"
        user.website_url = "https://example.com"
        user.save()
        profile = UserProfile.objects.create(user=user)
        profile.calculate_completion_percentage()
        self.assertEqual(profile.profile_completion_percentage, 100)
        self.assertTrue(profile.is_profile_complete)

    def test_calculate_completion_percentage_no_fields(self):
        user = CustomUser.objects.create(
            first_name="",
            last_name="",
            email="",
        )
        profile = UserProfile.objects.create(user=user)
        profile.calculate_completion_percentage()
        self.assertEqual(profile.profile_completion_percentage, 0)
        self.assertFalse(profile.is_profile_complete)

    def test_calculate_completion_percentage_some_fields(self):
        user = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        profile = UserProfile.objects.create(user=user)
        profile.calculate_completion_percentage()
        expected_percentage = (3 / 8) * 100
        self.assertEqual(profile.profile_completion_percentage, int(expected_percentage))
        self.assertFalse(profile.is_profile_complete)