from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.cache import cache_page

from homepage import views as home_view
from comment import views as comment_views
from django.contrib.auth import views as auth_views

from sitemaps.sitemaps import DisplayableSitemap
from django.contrib.sitemaps import views as sitemap_views

admin.autodiscover()

sitemaps = {"sitemaps": {"all": DisplayableSitemap}}

urlpatterns = [
    url(r'^$', home_view.homepage),
    url(r'^comment/$', comment_views.comment),
    url(r"^sitemap\.xml$", cache_page(60 * 60 * 6)(sitemap_views.sitemap), sitemaps),
    url(r"^admin/", include(admin.site.urls)),

    url("^", include("links.urls")),
    url("^", include("juba.urls")),
    url("^api/", include("api.urls")),
    url("^avatar/", include("avatar.urls")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),
    url(r'', include('social_django.urls', namespace='social')),
    url(r"^", include("mezzanine.urls")),
]

handler500 = "mezzanine.core.views.server_error"
