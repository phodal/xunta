from avatar.models import Avatar
from django.contrib.auth.models import User
from rest_framework import serializers

from user_profile.models import ProfileImage


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("avatar", "date_uploaded")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    avatar = AvatarSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = ("username", "avatar")


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)

    class Meta:
        model = ProfileImage
        fields = ('image', 'comments')
