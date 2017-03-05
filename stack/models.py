from django.urls import reverse
from django.db import models
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable, TimeStamped, MetaData
from mezzanine.generic.fields import RatingField
from django.utils.translation import ugettext_lazy as _

from xunta import settings

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Stack(Displayable):
    class Meta:
        verbose_name = _('堆栈')
        verbose_name_plural = _('堆栈')

    content = RichTextField(null=True, blank=(not getattr(settings, "Stack_REQUIRED", False)))
    rating = RatingField(blank=True)
    hot = models.IntegerField(blank=True)

    def get_absolute_url(self):
        return reverse("stack_detail", kwargs={"slug": self.slug})


class Job(MetaData, TimeStamped):
    class Meta:
        verbose_name = _('工作')
        verbose_name_plural = _('工作')

    name = models.CharField(max_length=50)
    content = RichTextField(null=True, blank=(not getattr(settings, "JOB_REQUIRED", False)))


class GitHubInfo(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    content = RichTextField()


class Company(Displayable):
    class Meta:
        verbose_name = _('公司')
        verbose_name_plural = _('公司')

    content = RichTextField(null=True, blank=(not getattr(settings, "Company_REQUIRED", False)))
    stacks = models.ForeignKey(Stack)
    jobs = models.ForeignKey(Job)

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"slug": self.slug})


class Programmer(models.Model):
    class Meta:
        verbose_name = _('程序员')
        verbose_name_plural = _('程序员')

    user = models.OneToOneField(USER_MODEL)
    current_stack = models.ForeignKey(Stack, related_name='current_stack')
    future_stack = models.ForeignKey(Stack, related_name='future_stack')
    contact = models.CharField(max_length=50)
    company = models.ForeignKey(Company, related_name='company')
    blog = models.SlugField()
