from __future__ import unicode_literals

from django.conf.urls import url

from stack.views import StackList

urlpatterns = [
    url("^$",
        StackList.as_view(),
        name="stack_home")
]
