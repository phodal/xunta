from mezzanine.blog.models import BlogPost
from rest_framework import serializers, viewsets
from rest_framework import filters


class BlogpostListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug')


class BlogPostListSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogpostListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')


class BlogpostDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'description', 'content')


class BlogPostDetailSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogpostDetailSerializer