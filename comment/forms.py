from __future__ import unicode_literals

from django_comments.forms import CommentForm
from django_comments.signals import comment_was_posted
from future.builtins import str

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.cache import add_cache_bypass
from mezzanine.utils.email import split_addresses, send_mail_template
from mezzanine.utils.views import ip_for_request
from django_markdown.widgets import MarkdownWidget


class ThreadedCommentForm(CommentForm, Html5Mixin):
    name = forms.CharField(label=_("Name"), help_text=_("required"),
                           max_length=50)
    email = forms.EmailField(label=_("Email"),
                             help_text=_("required (not published)"))
    url = forms.URLField(label=_("Website"), help_text=_("optional"),
                         required=False)

    comment = forms.CharField(label=_('Comment'), widget=MarkdownWidget(),
                              max_length=300)

    # These are used to get/set prepopulated fields via cookies.
    cookie_fields = ("name", "email", "url")
    cookie_prefix = "mezzanine-comment-"

    class Meta:
        model = ThreadedComment
        fields = ('comment',)

    def __init__(self, request, *args, **kwargs):
        """
        Set some initial field values from cookies or the logged in
        user, and apply some HTML5 attributes to the fields if the
        ``FORMS_USE_HTML5`` setting is ``True``.
        """
        kwargs.setdefault("initial", {})
        user = request.user
        for field in ThreadedCommentForm.cookie_fields:
            cookie_name = ThreadedCommentForm.cookie_prefix + field
            value = request.COOKIES.get(cookie_name, "")
            if not value and user.is_authenticated():
                if field == "name":
                    value = user.get_full_name()
                    if not value and user.username != user.email:
                        value = user.username
                elif field == "email":
                    value = user.email
            kwargs["initial"][field] = value
        super(ThreadedCommentForm, self).__init__(*args, **kwargs)

    def get_comment_model(self):
        """
        Use the custom comment model instead of the built-in one.
        """
        return ThreadedComment

    def save(self, request):
        """
        Saves a new comment and sends any notification emails.
        """
        comment = self.get_comment_object()
        obj = comment.content_object
        if request.user.is_authenticated():
            comment.user = request.user
        comment.by_author = request.user == getattr(obj, "user", None)
        comment.ip_address = ip_for_request(request)
        comment.replied_to_id = self.data.get("replied_to")
        comment.save()
        comment_was_posted.send(sender=comment.__class__, comment=comment,
                                request=request)
        notify_emails = split_addresses(settings.COMMENTS_NOTIFICATION_EMAILS)
        if notify_emails:
            subject = ugettext("New comment for: ") + str(obj)
            context = {
                "comment": comment,
                "comment_url": add_cache_bypass(comment.get_absolute_url()),
                "request": request,
                "obj": obj,
            }
            send_mail_template(subject, "email/comment_notification",
                               settings.DEFAULT_FROM_EMAIL, notify_emails,
                               context)
        return comment
