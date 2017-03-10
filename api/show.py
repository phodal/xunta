from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.common_serializer import UserSerializer
from show.models import Show


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Show
        fields = ('title', 'user', 'image', 'posted_on')


class ShowSet(viewsets.ModelViewSet):
    queryset = Show.objects.filter()
    serializer_class = ShowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', )
