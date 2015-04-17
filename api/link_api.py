from rest_framework import serializers, viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from links.models import Link

class LinkListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('title', 'slug')


class LinkListSet(viewsets.ReadOnlyModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')


class LinkDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('title', 'slug', 'url', 'description')


class LinkDetailSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkDetailSerializer
    permission_classes = (IsAuthenticated,)