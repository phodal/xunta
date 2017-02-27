from django.contrib import admin
from django.contrib.admin import ModelAdmin

from user_profile.models import Profile


class ProfileAdmin(ModelAdmin):
    list_display = ("id", "user", "job", "address", "birthday")
    list_display_links = ("id",)


admin.site.register(Profile, ProfileAdmin)
