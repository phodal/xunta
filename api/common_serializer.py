from avatar.models import Avatar
from django.contrib.auth.models import User
from rest_framework import serializers

from user_profile.models import ProfileImage


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("avatar", )


class UserSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = User
        fields = ("username", "avatar")


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)

    class Meta:
        model = ProfileImage
        fields = ('image', 'comments')
