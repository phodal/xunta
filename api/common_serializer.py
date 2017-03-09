from django.contrib.auth.models import User
from rest_framework import serializers

from user_profile.models import ProfileImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", )


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)

    class Meta:
        model = ProfileImage
        fields = ('image', 'comments')
