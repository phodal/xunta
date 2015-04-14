from django.conf.urls import url, include
from mezzanine.blog.models import BlogPost
from rest_framework import serializers, viewsets, routers
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

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'blog', BlogPostListSet)
router.register(r'list', BlogPostDetailSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]