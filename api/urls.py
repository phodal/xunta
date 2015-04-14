from django.conf.urls import url, include
from rest_framework import routers

from api.blog_api import BlogPostListSet, BlogPostDetailSet


router = routers.DefaultRouter()
router.register(r'blog', BlogPostListSet)
router.register(r'list', BlogPostDetailSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]