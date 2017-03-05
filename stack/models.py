from django.urls import reverse
from django.db import models
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable
from mezzanine.generic.fields import RatingField
from django.utils.translation import ugettext_lazy as _

from xunta import settings


class Stack(Displayable):
    class Meta:
        verbose_name = _('堆栈')
        verbose_name_plural = _('堆栈')

    content = RichTextField(null=True, blank=(not getattr(settings, "Stack_REQUIRED", False)))
    rating = RatingField(blank=True)
    hot = models.IntegerField(blank=True)

    def get_absolute_url(self):
        return reverse("stack_detail", kwargs={"slug": self.slug})
