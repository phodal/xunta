import json

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth import login
from mezzanine.accounts import get_profile_form
from mezzanine.accounts.forms import LoginForm, ProfileForm
from mezzanine.utils.urls import login_redirect
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa
from django.contrib.messages import info
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (login as auth_login,
                                 logout as auth_logout)
from django.contrib.auth.decorators import login_required
from mezzanine.utils.views import render

from auth.decorators import render_to


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


def context(**extra):
    return dict({
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)


def login(request, template="accounts/account_login.html"):
    """
    Login form.
    """
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        authenticated_user = form.save()
        info(request, _("Successfully logged in"))
        auth_login(request, authenticated_user)
        return login_redirect(request)
    context = {"form": form, "title": _("Log in")}
    return render(request, template, context)


@login_required
@render_to('accounts/account_profile.html')
def done(request):
    """Login complete view, displays user data"""
    return context()


@login_required
def newuser(request, template="accounts/account_profile_update.html"):
    """
    Profile update form.
    """
    profile_form = ProfileForm
    form = profile_form(request.POST or None, request.FILES or None,
                        instance=request.user)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        info(request, _("Profile updated"))
        try:
            return redirect("profile", username=user.username)
        except NoReverseMatch:
            return redirect("profile_update")
    context = {"form": form, "title": _("Update Profile")}
    return render(request, template, context)


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')
