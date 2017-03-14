from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from juba.models import Juba


class JubaDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField('get_username_by_id')
    date = serializers.SerializerMethodField('get_special_date')

    @staticmethod
    def get_username_by_id(model):
        user = User.objects.get(id=model.user_id)
        return user.get_full_name()


    @staticmethod
    def get_special_date(model):
        return model.publish_date.strftime('%Y-%m-%d')

    class Meta:
        model = Juba
        fields = ('title', 'slug', 'description', 'content', 'id', 'date', 'user')


class JubaSet(viewsets.ModelViewSet):
    queryset = Juba.objects.filter(status=2)
    serializer_class = JubaDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
