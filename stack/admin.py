from django.contrib import admin

from stack.models import Stack, Company, Programmer, GitHubInfo, Job


admin.site.register(Stack)
admin.site.register(Company)
admin.site.register(Programmer)
admin.site.register(GitHubInfo)
admin.site.register(Job)
