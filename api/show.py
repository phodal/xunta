from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.common_serializer import UserSerializer

from show.models import Show


class ShowGetSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Show
        fields = ('title', 'user', 'image', 'posted_on')


class ShowPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = ('title', 'image', 'posted_on')


class ShowSet(viewsets.ModelViewSet):
    queryset = Show.objects.filter()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ShowPostSerializer
        return ShowGetSerializer
