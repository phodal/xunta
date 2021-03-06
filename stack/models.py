from django.template.defaultfilters import truncatewords_html
from django.urls import reverse
from django.db import models
from django.utils.html import strip_tags
from imagekit.models import ProcessedImageField
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable, TimeStamped, MetaData, Slugged
from mezzanine.generic.fields import RatingField
from django.utils.translation import ugettext_lazy as _
from mezzanine.utils.html import TagCloser

from xunta import settings

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Category(Slugged, TimeStamped):
    content = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name = _("分类")
        verbose_name_plural = _("分类")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return "stack_category", (), {"category": self.slug}


class Stack(Slugged, TimeStamped):
    class Meta:
        verbose_name = _('技术栈')
        verbose_name_plural = _('技术栈')

    content = RichTextField(null=True, blank=(not getattr(settings, "Stack_REQUIRED", False)))
    rating = RatingField(null=True, blank=True, verbose_name='评价')
    hot = models.IntegerField(null=True, blank=True, verbose_name='热度')
    featured_image = ProcessedImageField(null=True, blank=True, upload_to='stack', format='JPEG', options={'quality': 100})
    category = models.ManyToManyField("Category",
                                      verbose_name=_("分类"),
                                      blank=True, related_name="category")
    description = models.TextField(_("Description"), blank=True)

    def get_absolute_url(self):
        return reverse("stack_detail", kwargs={"slug": self.slug})

    def description_from_content(self):
        """
        Returns the first block or sentence of the first content-like
        field.
        """
        description = ""
        # Use the first RichTextField, or TextField if none found.
        for field_type in (RichTextField, models.TextField):
            if not description:
                for field in self._meta.fields:
                    if (isinstance(field, field_type) and
                                field.name != "description"):
                        description = getattr(self, field.name)
                        if description:
                            from mezzanine.core.templatetags.mezzanine_tags \
                                import richtext_filters
                            description = richtext_filters(description)
                            break
        # Fall back to the title if description couldn't be determined.
        if not description:
            description = str(self)
        # Strip everything after the first block or sentence.
        ends = ("</p>", "<br />", "<br/>", "<br>", "</ul>",
                "\n", ". ", "! ", "? ")
        for end in ends:
            pos = description.lower().find(end)
            if pos > -1:
                description = TagCloser(description[:pos]).html
                break
        else:
            description = truncatewords_html(description, 100)
        try:
            description = unicode(description)
        except NameError:
            pass  # Python 3.
        return description

    def save(self, *args, **kwargs):
        """
        Set the description field on save.
        """
        self.description = strip_tags(self.description_from_content())
        super(Stack, self).save(*args, **kwargs)


class Job(MetaData, TimeStamped):
    class Meta:
        verbose_name = _('工作')
        verbose_name_plural = _('工作')

    content = models.TextField(_("内容"), blank=True)
    name = models.CharField(max_length=50, verbose_name="一行介绍")
    province = models.CharField(blank=True, max_length=10, verbose_name="省")
    cities = models.CharField(blank=True, max_length=10, verbose_name="市")
    zone = models.CharField(blank=True, max_length=10, verbose_name="区")
    address = models.CharField(blank=True, max_length=10, verbose_name="地址")
    salary_start = models.IntegerField(blank=True, default=0, verbose_name="待遇（始）")
    salary_end = models.IntegerField(blank=True, default=0, verbose_name="待遇（到）")
    stacks = models.ManyToManyField("Stack",
                                    verbose_name=_("技术栈"),
                                    blank=True, related_name="job_stacks")

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
    stacks = models.ManyToManyField("Stack",
                                    verbose_name=_("技术栈"),
                                    blank=True, related_name="company_stacks")
    jobs = models.ManyToManyField("Job",
                                  verbose_name=_("相关工作"),
                                  blank=True, related_name="jobs")

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"slug": self.slug})


class Programmer(models.Model):
    class Meta:
        verbose_name = _('程序员')
        verbose_name_plural = _('程序员')

    user = models.OneToOneField(USER_MODEL)
    current_stack = models.ManyToManyField("Stack",
                                     verbose_name=_("当前技术栈"),
                                     blank=True, related_name="current_stack")
    future_stack = models.ManyToManyField("Stack",
                                     verbose_name=_("未来技术栈"),
                                     blank=True, related_name="future_stack")

    contact = models.CharField(max_length=50)
    company = models.ManyToManyField("Company",
                                     verbose_name=_("公司"),
                                     blank=True, related_name="company")
    blog = models.SlugField()
