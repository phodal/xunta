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
        exclude = (get_profile_user_fieldname(), "following",) + _exclude_fields


if settings.ACCOUNTS_NO_USERNAME:
    _exclude_fields += ("username",)
    username_label = _("Email address")
else:
    username_label = _("Username or email address")


class ProfileForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """

    birthday = DateField(widget=AdminDateWidget)

    class Meta:
        model = User
        fields = ("first_name", "last_name")
        exclude = _exclude_fields

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = set([f.name for f in User._meta.get_fields()])
        try:
            self.fields["username"].help_text = ugettext(
                        "Only letters, numbers, dashes or underscores please")
        except KeyError:
            pass
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True

        # Add any profile fields to the form.
        profile_fields_form = self.get_profile_fields_form()
        profile_fields = profile_fields_form().fields
        self.fields.update(profile_fields)
        if not self._signup:
            user_profile = get_profile_for_user(self.instance)
            for field in profile_fields:
                value = getattr(user_profile, field)
                # Check for multiple initial values, i.e. a m2m field
                if isinstance(value, Manager):
                    value = value.all()
                self.initial[field] = value

    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        if username.lower() != slugify(username).lower():
            raise forms.ValidationError(
                ugettext("Username can only contain letters, numbers, dashes "
                         "or underscores."))
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
                            ugettext("This username is already registered"))

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(
                                ugettext("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """

        kwargs["commit"] = False
        user = super(ProfileForm, self).save(*args, **kwargs)
        try:
            self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                try:
                    username = ("%(first_name)s %(last_name)s" %
                                self.cleaned_data).strip()
                except KeyError:
                    username = ""
                if not username:
                    username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify(username))
        user.save()

        profile = get_profile_for_user(user)
        profile_form = self.get_profile_fields_form()
        profile_form(self.data, self.files, instance=profile).save()

        if self._signup:
            if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
                    settings.ACCOUNTS_APPROVAL_REQUIRED):
                user.is_active = False
                user.save()
            else:
                token = default_token_generator.make_token(user)
                user = authenticate(uidb36=int_to_base36(user.id),
                                    token=token,
                                    is_active=True)
        return user

    def get_profile_fields_form(self):
        try:
            return ProfileFieldsForm
        except NameError:
            raise ProfileNotConfigured
