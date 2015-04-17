from django.conf.urls import url, include
from rest_framework import routers

from api.blog_api import BlogPostListSet, BlogPostDetailSet
from api.juba_api import JubaListSet, JubaDetailSet
from api.link_api import LinkListSet, LinkDetailSet
from api.views import AllListView

router = routers.DefaultRouter()
router.register(r'blog_list', BlogPostListSet)
router.register(r'juba_list', JubaListSet)
router.register(r'link_list', LinkListSet)

router.register(r'blog_detail', BlogPostDetailSet)
router.register(r'juba_detail', JubaDetailSet)
router.register(r'link_detail', LinkDetailSet)

router.register(r'all', AllListView, 'all')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]