from django.contrib import admin

from show.models import Show, Like, Comment

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Show)
