from __future__ import unicode_literals

from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.manager import Manager
from django.forms import DateField, DateTimeField
from django.utils.http import int_to_base36
from django.utils.translation import ugettext, ugettext_lazy as _
from mezzanine.accounts import (get_profile_model, get_profile_user_fieldname,
                                get_profile_for_user, ProfileNotConfigured)
from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin
from mezzanine.utils.urls import slugify, unique_slug

from user_profile.models import Profile

User = get_user_model()

_exclude_fields = tuple(getattr(settings,
                                "ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS", ()))


class ProfileFieldsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = (get_profile_user_fieldname(), "following", "follows") + _exclude_fields


if settings.ACCOUNTS_NO_USERNAME:
    _exclude_fields += ("username",)
    username_label = _("Email address")
else:
    username_label = _("Username or email address")
