from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from links.models import Link


class LinkDetailSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField('get_special_date')
    
    @staticmethod
    def get_special_date(model):
        return model.publish_date.strftime('%Y-%m-%d')

    class Meta:
        model = Link
        fields = ('title', 'slug', 'link', 'id', 'date')


class LinkDetailSet(viewsets.ModelViewSet):
    queryset = Link.objects.filter(status=2)
    serializer_class = LinkDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')
