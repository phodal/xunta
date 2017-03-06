from django.urls import reverse
from django.db import models
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable, TimeStamped, MetaData, Slugged
from mezzanine.generic.fields import RatingField
from django.utils.translation import ugettext_lazy as _

from xunta import settings

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Stack(Slugged, TimeStamped):
    class Meta:
        verbose_name = _('技术栈')
        verbose_name_plural = _('技术栈')

    content = RichTextField(null=True, blank=(not getattr(settings, "Stack_REQUIRED", False)))
    rating = RatingField(null=True, blank=True, verbose_name='评价')
    hot = models.IntegerField(null=True, blank=True, verbose_name='热度')

    def get_absolute_url(self):
        return reverse("stack_detail", kwargs={"slug": self.slug})


class Job(MetaData, TimeStamped):
    class Meta:
        verbose_name = _('工作')
        verbose_name_plural = _('工作')

    name = models.CharField(max_length=50, verbose_name="一行介绍")
    province = models.CharField(blank=True, max_length=10, verbose_name="省")
    cities = models.CharField(blank=True, max_length=10, verbose_name="市")
    zone = models.CharField(blank=True, max_length=10, verbose_name="区")
    address = models.CharField(blank=True, max_length=10, verbose_name="地址")
    salary_start = models.IntegerField(blank=True, default=0, verbose_name="待遇（始）")
    salary_end = models.IntegerField(blank=True, default=0, verbose_name="待遇（到）")


class GitHubInfo(models.Model):
    class Meta:
        verbose_name = _('GitHub项目')
        verbose_name_plural = _('GitHub项目')

    name = models.CharField(max_length=50)
    slug = models.SlugField()
    content = RichTextField()


class Company(Slugged, TimeStamped):
    class Meta:
        verbose_name = _('公司')
        verbose_name_plural = _('公司')

    content = RichTextField(null=True, blank=(not getattr(settings, "Company_REQUIRED", False)))
    stacks = models.ForeignKey(Stack, blank=True, null=True)
    jobs = models.ForeignKey(Job, blank=True, null=True)

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
