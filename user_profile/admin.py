from django.contrib import admin
from django.contrib.admin import ModelAdmin

from user_profile.models import Profile, ProfileImage


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 3


class ProfileAdmin(ModelAdmin):
    list_display = ("id", "user", "job", "address", "birthday")
    list_display_links = ("id",)
    inlines = [ProfileImageInline, ]


admin.site.register(Profile, ProfileAdmin)
