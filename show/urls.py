from __future__ import unicode_literals

from django.conf.urls import url
from show import views as show_view

urlpatterns = [
    url("^$",show_view.index, name="link_home"),
]
