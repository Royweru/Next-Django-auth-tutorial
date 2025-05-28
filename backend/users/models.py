from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

def generate_user_id():
    return str(uuid.uuid4())

class CustomUserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
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
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Disable username field
    id = models.CharField(max_length=36, primary_key=True, default=generate_user_id, editable=False)
    
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500, null=True)
    is_newsletter_subscribed = models.BooleanField(default=False)
    
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    email_verified = models.BooleanField(default=False)
    
    # Fix the reverse accessor clash by adding related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    # Add the custom manager
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Remove 'username' from here!

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate_user_id()
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    is_profile_complete = models.BooleanField(default=False)
    profile_completion_percentage = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.get_full_name()} Profile"
    
    def calculate_completion_percentage(self):
        """
        Calculate the profile completion percentage based on filled fields.
        """
        fields_to_check = [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.user.profile_picture,
            self.user.bio,
            self.user.linkedin_url,
            self.user.github_url,
            self.user.website_url
        ]
        completed_fields = sum(1 for field in fields_to_check if field)
        total_fields = len(fields_to_check)
        percentage = (completed_fields / total_fields) * 100
        self.profile_completion_percentage = int(percentage)
        self.is_profile_complete = percentage == 100
        self.save()