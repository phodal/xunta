from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Profile(models.Model):
    class Meta:
        verbose_name = _('个人信息')
        verbose_name_plural = _('个人信息')

    YEAR_IN_SCHOOL_CHOICES = (
        ('1', '白羊座'),
        ('2', '金牛座'),
        ('3', '双子座'),
        ('4', '巨蟹座'),
        ('5', '狮子座'),
        ('6', '处女座'),
        ('7', '天秤座'),
        ('8', '天蝎座'),
        ('9', '射手座'),
        ('10', '摩羯座'),
        ('11', '双鱼座'),
        ('12', '双鱼座'),
    )

    user = models.OneToOneField(USER_MODEL)
    address = models.CharField(blank=True, max_length=20, verbose_name=_('地址'))
    birthday = models.DateTimeField(_("生日"), help_text=_(""), blank=True, null=True, db_index=True)
    interest = models.CharField(blank=True,  max_length=20, verbose_name=_('爱好'))
    weight = models.IntegerField(default=150, blank=True, verbose_name=_('体重'))
    height = models.IntegerField(default=150, blank=True, verbose_name=_('身高'))
    constellate = models.CharField(blank=True, max_length=10, choices=YEAR_IN_SCHOOL_CHOICES, verbose_name=_('星座'))
    job = models.CharField(blank=True, max_length=10, verbose_name=_('职业'))
    movie_type = models.CharField(blank=True, max_length=10, verbose_name=_('电影类型'))
    sport_type = models.CharField(blank=True, max_length=10, verbose_name=_('运动爱好'))
    book_type = models.CharField(blank=True, max_length=10, verbose_name=_('书籍类型'))
    karma = models.IntegerField(default=0, editable=False)
    bio = models.TextField(blank=True, verbose_name=_('简介'))
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    following = models.ManyToManyField('self', related_name="following_profile", blank=True)

    def __str__(self):
        return "%s (%s)" % (self.user, self.karma)
