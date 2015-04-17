from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
import mezzanine_pagedown.urls
from sitemaps.sitemaps import DisplayableSitemap

admin.autodiscover()

urlpatterns = patterns("homepage.views",
    url("^$", "homepage", name="home"),
)

urlpatterns += patterns("comment.views",
    url("^comment/$", "comment", name="comment"),
)


sitemaps = {"sitemaps": {"all": DisplayableSitemap}}
urlpatterns += patterns("django.contrib.sitemaps.views",
    ("^sitemap\.xml$", "sitemap", sitemaps)
)

urlpatterns += patterns("",
    ("^admin/", include(admin.site.urls)),
    ("^", include("links.urls")),
    ("^", include("juba.urls")),
    ("^api/", include("api.urls")),
    ("^avatar/", include("avatar.urls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'auth.views.login'),
    url(r'^logout/$', 'auth.views.logout'),
    url(r'^done/$', 'auth.views.done', name='done'),
    url(r'^new-users-redirect-url/$', 'auth.views.newuser'),
    url("^pagedown/", include(mezzanine_pagedown.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    ("^", include("mezzanine.urls")),
)

handler500 = "mezzanine.core.views.server_error"
