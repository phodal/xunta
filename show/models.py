from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField

from user_profile.models import Profile
from django.utils.translation import ugettext_lazy as _


class Show(models.Model):
    class Meta:
        verbose_name = _('秀吧')
        verbose_name_plural = _('秀吧')

    user_profile = models.ForeignKey(Profile, null=True, blank=True)
    title = models.CharField(max_length=100)
    image = ProcessedImageField(upload_to='show',
                                format='JPEG',
                                options={'quality': 100})
    posted_on = models.DateTimeField(default=datetime.now)

    def get_number_of_likes(self):
        return self.like_set.count()

    def get_number_of_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Show')
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.comment


class Like(models.Model):
    post = models.ForeignKey('Show')
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _('赞')
        verbose_name_plural = _("赞")
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title
