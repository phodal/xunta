from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost
from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class BlogpostDetailSerializer(serializers.HyperlinkedModelSerializer):
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
        model = BlogPost
        fields = ('title', 'slug', 'description', 'content', 'id', 'date', 'user')


class BlogPostDetailSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(status=2)
    serializer_class = BlogpostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')
