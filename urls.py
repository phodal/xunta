from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("homepage.views",
    # url("^$", "homepage", name="home"),
)

urlpatterns += patterns("",
    ("^admin/", include(admin.site.urls)),
    ("^", include("links.urls")),
    ("^", include("juba.urls")),
    ("^api/", include("api.urls")),
    ("^avatar/", include("avatar.urls")),
    url(r'^$', 'app.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email-sent/', 'app.views.validation_sent'),
    url(r'^login/$', 'app.views.home'),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^done/$', 'app.views.done', name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'app.views.ajax_auth', name='ajax-auth'),
    url(r'^email/$', 'app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    ("^", include("mezzanine.urls")),
)

handler500 = "mezzanine.core.views.server_error"
