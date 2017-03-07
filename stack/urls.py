from __future__ import unicode_literals

from django.conf.urls import url

from stack.views import StackList, StackDetail, CompanyDetail

urlpatterns = [
    url("^stack/$",
        StackList.as_view(),
        name="stack_home"),
    url("^stack/(?P<slug>.*)/$",
        StackDetail.as_view(),
        name="stack_detail"),
    url("^company/(?P<slug>.*)/$",
        CompanyDetail.as_view(),
        name="company_detail"),
]
