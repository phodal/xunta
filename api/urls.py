from django.conf.urls import url, include
from rest_framework import routers

from api.blog import BlogPostDetailSet
from api.juba import JubaDetailSet
from api.link import LinkSet
from api.profile import ProfileSet
from api.show import ShowSet
from api.stack import StackSet
from api.user import UserSet
from api.views import AllListView

router = routers.DefaultRouter()

router.register(r'blog', BlogPostDetailSet)
router.register(r'juba', JubaDetailSet)
router.register(r'link', LinkSet)
router.register(r'stack', StackSet)
router.register(r'show', ShowSet)
router.register(r'user', UserSet)
router.register(r'profile', ProfileSet)

router.register(r'home', AllListView, 'home')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
