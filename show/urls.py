from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from show import views as show_view
from show.views import ShowCreate

urlpatterns = [
    url("^$",show_view.index, name="link_home"),
    url("^users/(?P<username>.*)/juba/$",
        show_view.index, {"by_score": False},
        name="show_list_user"),
    url("^create/$",
        login_required(ShowCreate.as_view()),
        name="show_create"),
]
