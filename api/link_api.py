from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from links.models import Link

class LinkListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('title', 'slug')


class LinkListSet(viewsets.ReadOnlyModelViewSet):
    queryset = Link.objects.filter(status=2)
    serializer_class = LinkListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')


class LinkDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField('get_username_by_id')

    @staticmethod
    def get_username_by_id(model):
        user = User.objects.get(id=model.user_id)
        return user.username

    class Meta:
        model = Link
        fields = ('title', 'slug', 'url', 'description', 'id', 'publish_date', 'user')


class LinkDetailSet(viewsets.ModelViewSet):
    queryset = Link.objects.filter(status=2)
    serializer_class = LinkDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')