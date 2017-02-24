from django.conf.urls import url, include
from rest_framework import routers

from api.blog_api import BlogPostDetailSet
from api.juba_api import JubaDetailSet
from api.link_api import LinkDetailSet
from api.views import AllListView

router = routers.DefaultRouter()

router.register(r'blog', BlogPostDetailSet)
router.register(r'juba', JubaDetailSet)
router.register(r'link', LinkDetailSet)

router.register(r'all', AllListView, 'all')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
