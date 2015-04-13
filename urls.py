from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("homepage.views",
    url("^$", "homepage", name="home"),
)

urlpatterns += patterns("",
    ("^admin/", include(admin.site.urls)),
    ("^", include("drum.links.urls")),
    ("^", include("juba.urls")),
    ("^", include("mezzanine.urls")),
)

handler500 = "mezzanine.core.views.server_error"
