from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin

from stack.models import Stack, Company, Programmer, GitHubInfo, Job


class StackAdmin(DisplayableAdmin):
    list_display = ("id", "title", "content", "status", "hot", "rating")

admin.site.register(Stack, StackAdmin)
admin.site.register(Company)
admin.site.register(Programmer)
admin.site.register(GitHubInfo)
admin.site.register(Job)
