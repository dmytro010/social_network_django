from django.contrib import admin
from .models import Post, User, PostLike
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(PostLike)



