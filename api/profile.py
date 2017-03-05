from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user_profile.models import Profile, ProfileImage


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)

    class Meta:
        model = ProfileImage
        fields = ('image', 'comments')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField('get_username_by_id')
    images = ProfileImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'birthday', 'constellate', 'height', 'interest', 'images')

    @staticmethod
    def get_username_by_id(model):
        user = User.objects.get(id=model.user_id)
        return user.get_full_name()


class ProfileSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
