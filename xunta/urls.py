from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.views.i18n import set_language
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from homepage import views as home_view
from comment import views as comment_views
from django.contrib.auth import views as auth_views

from sitemaps.sitemaps import DisplayableSitemap
from django.contrib.sitemaps import views as sitemap_views

from xunta import settings

admin.autodiscover()

sitemaps = {"sitemaps": {"all": DisplayableSitemap}}

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]


urlpatterns = [
    url(r'^$', home_view.homepage, name='home'),
    url(r'^comment/$', comment_views.comment),
    url(r"^sitemap\.xml$", sitemap_views.sitemap, sitemaps),

    url("^link/", include("links.urls")),
    url("^juba/", include("juba.urls")),
    url("^show/", include("show.urls")),
    url("^", include("stack.urls")),
    url("^api/", include("api.urls")),
    url("^avatar/", include("avatar.urls")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),

    url(r'^api/token/auth/', obtain_jwt_token),
    url(r'^api/token/refresh/', refresh_jwt_token),

    url('', include('social_django.urls', namespace='social')),
    url(r'', include('social_django.urls', namespace='social')),
    url(r"^", include("mezzanine.urls")),
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
