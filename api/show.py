from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from show.models import Show


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = ('title', 'image', 'posted_on')


class ShowSet(viewsets.ModelViewSet):
    queryset = Show.objects.filter()
    serializer_class = ShowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
