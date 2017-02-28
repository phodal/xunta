from __future__ import unicode_literals

from django.conf.urls import url
from show import views as show_view

urlpatterns = [
    url("^$",show_view.index, name="link_home"),
    url("^users/(?P<username>.*)/juba/$",
        show_view.index, {"by_score": False},
        name="show_list_user"),

]
