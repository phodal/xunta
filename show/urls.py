from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from show.views import ShowCreate, ShowDetail, ShowList

urlpatterns = [
    url("^$",
        ShowList.as_view(),
        name="show_home"),
    url("^create/$",
        login_required(ShowCreate.as_view()),
        name="show_create"),
    url("^show/(?P<slug>.*)/$",
        ShowDetail.as_view(),
        name="show_detail"),

]
