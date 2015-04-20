from rest_framework import serializers, viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from juba.models import Juba


class JubaListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Juba
        fields = ('title', 'slug')


class JubaListSet(viewsets.ModelViewSet):
    queryset = Juba.objects.filter(status=2)
    serializer_class = JubaListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')


class JubaDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Juba
        fields = ('title', 'slug', 'description', 'content', 'id', 'publish_date')


class JubaDetailSet(viewsets.ModelViewSet):
    queryset = Juba.objects.filter(status=2)
    serializer_class = JubaDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')