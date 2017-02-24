from __future__ import unicode_literals

from functools import reduce
from operator import ior
from string import punctuation

from future.builtins import int
from mezzanine.accounts import get_profile_model
from mezzanine.core.fields import RichTextField

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.core.models import Displayable, Ownable
from mezzanine.core.request import current_request
from mezzanine.generic.models import Rating, Keyword, AssignedKeyword
from mezzanine.generic.fields import RatingField, CommentsField
from uuslug import uuslug

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Juba(Displayable, Ownable):
    content = RichTextField(null=True,
                        blank=(not getattr(settings, "JUBA_REQUIRED", False)))
    rating = RatingField()
    comments = CommentsField()

    def get_absolute_url(self):
        return reverse("juba_detail", kwargs={"slug": self.slug})

    @property
    def domain(self):
        return urlparse(self.url).netloc

    @property
    def url(self):
        if self.content:
            return self.content
        return current_request().build_absolute_uri(self.get_absolute_url())

    def save(self, *args, **kwargs):
        keywords = []
        self.slug = uuslug(self.title, instance=self)
        if not self.keywords_string and getattr(settings, "AUTO_TAG", False):
            keywords = self.title.rstrip(punctuation).split()
        super(Juba, self).save(*args, **kwargs)
        if keywords:
            lookup = reduce(ior, [Q(title__iexact=k) for k in keywords])
            for keyword in Keyword.objects.filter(lookup):
                self.keywords.add(AssignedKeyword(keyword=keyword))


@receiver(post_save, sender=Rating)
def karma(sender, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2.
    """
    rating = kwargs["instance"]
    value = int(rating.value)
    if not kwargs["created"]:
        value *= 2
    content_object = rating.content_object
    if rating.user != content_object.user:
        queryset = get_profile_model().objects.filter(user=content_object.user)
        queryset.update(karma=models.F("karma") + value)
