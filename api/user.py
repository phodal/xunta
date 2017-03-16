from django.contrib.auth.models import User
from rest_condition import Or
from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAdminUser

from api.permissions.is_admin_or_self import IsPostRequest


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    permission_classes = [Or(IsAdminUser, IsPostRequest)]
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserPostSerializer
        return UserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
