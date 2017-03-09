from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.common_serializer import UserSerializer, ProfileImageSerializer
from user_profile.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)
    constellate = serializers.SerializerMethodField()
    images = ProfileImageSerializer(many=True, required=False, read_only=True)

    def get_constellate(self, obj):
        return obj.get_constellate_display()

    class Meta:
        model = Profile
        fields = ('user', 'birthday', 'constellate', 'bio', 'height', 'interest', 'images')


class ProfileSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
