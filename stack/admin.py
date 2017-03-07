from django.contrib import admin
from django.contrib.admin import ModelAdmin

from stack.models import Stack, Company, Programmer, GitHubInfo, Job, Category


class StackAdmin(ModelAdmin):
    list_display = ("id", "title", "slug", "created")
    list_display_links = ("id",)
    exclude = ('description',)
    filter_horizontal = ("category",)
    fieldsets = [
        (None, {'fields': [('title', "category", 'slug', "content", "hot", "featured_image")]}),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


class CompanyAdmin(ModelAdmin):
    list_display = ("id", "title", "slug", "created")
    list_display_links = ("id",)
    filter_horizontal = ("stacks", "jobs",)


class ProgrammerAdmin(ModelAdmin):
    list_display = ("id", "blog",)
    filter_horizontal = ("current_stack", "future_stack", "company")


class JobAdmin(ModelAdmin):
    list_display = ("id", "name", "salary_start", "salary_end")
    list_display_links = ("id", )
    filter_horizontal = ("stacks",)
    fieldsets = [
        (None, {'fields': [('name', "content", "province", 'cities', "zone", "address", "salary_start", "salary_end", "stacks")]}),
    ]


admin.site.register(Stack, StackAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Category)
admin.site.register(Programmer, ProgrammerAdmin)
admin.site.register(GitHubInfo)
admin.site.register(Job, JobAdmin)
