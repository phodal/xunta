from django.contrib import admin
from mezzanine.core.admin import OwnableAdmin

from show.models import Show, Like, Comment

class ShowAmin(OwnableAdmin):

    list_display = ("id", "title", "user", "posted_on")
    ordering = ("-posted_on",)

    fieldsets = (
        (None, {
            "fields": ("title", "image"),
        }),
    )

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Show, ShowAmin)
