from django.contrib import admin
from .models import User, Post, Like
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('author',)

admin.site.register(Post, PostAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')

admin.site.register(Like, LikeAdmin)