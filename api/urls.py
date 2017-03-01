from django.conf.urls import url, include
from rest_framework import routers

from api.blog import BlogPostDetailSet
from api.juba import JubaDetailSet
from api.link import LinkDetailSet
from api.profile import ProfileSet
from api.views import AllListView

router = routers.DefaultRouter()

router.register(r'blog', BlogPostDetailSet)
router.register(r'juba', JubaDetailSet)
router.register(r'link', LinkDetailSet)
router.register(r'profile', ProfileSet)

router.register(r'home', AllListView, 'home')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
