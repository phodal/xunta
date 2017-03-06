from __future__ import unicode_literals

from django.conf.urls import url

from stack.views import StackList, StackDetail

urlpatterns = [
    url("^$",
        StackList.as_view(),
        name="stack_home"),
    url("^(?P<slug>.*)/$",
        StackDetail.as_view(),
        name="stack_detail"),
]
