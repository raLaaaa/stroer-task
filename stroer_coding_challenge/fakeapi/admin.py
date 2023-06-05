from django.contrib import admin

from fakeapi.models import models
from fakeapi.models import Comment, Post

admin.site.register(Post)
admin.site.register(Comment)
