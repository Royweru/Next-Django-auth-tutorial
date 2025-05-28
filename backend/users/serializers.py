from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = None
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2= serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ( 'email', 'password', 'password2','first_name', 'last_name', )
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
           ' password':{'write_only': True, 'required': True, 'validators': [validate_password]},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)  # Create a UserProfile instance
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    profile_completion_percentage = serializers.ReadOnlyField(source='profile.profile_completion_percentage')
    is_profile_complete = serializers.ReadOnlyField(source='profile.is_profile_complete')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name',
             'bio', 'profile_picture',
            'is_newsletter_subscribed','website_url',
            'github_url', 'linkedin_url',
            'profile_completion_percentage', 'is_profile_complete'
        )
        read_only_fields = ('id', 'email', 'profile_completion_percentage', 'is_profile_complete')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('first_name', 'last_name', 'bio', 'profile_picture', 'is_newsletter_subscribed', 'website_url', 'github_url', 'linkedin_url')
        read_only_fields = ('id','email','created_at','updated_at', 'profile_completion_percentage', 'is_profile_complete')
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # Recalculate profile completion
        user.profile.calculate_completion_percentage()
        return user

