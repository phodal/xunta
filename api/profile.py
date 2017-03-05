from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.common_serializer import UserSerializer, ProfileImageSerializer
from user_profile.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)
    images = ProfileImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'birthday', 'constellate', 'height', 'interest', 'images')


class ProfileSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
