from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from stack.models import Stack


class StackAdmin(DisplayableAdmin):
    list_display = ("id", "title", "content", "status", "hot", "rating")

admin.site.register(Stack, StackAdmin)
