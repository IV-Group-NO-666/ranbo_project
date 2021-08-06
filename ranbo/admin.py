from django.contrib import admin
from ranbo.models import UserProfile
from ranbo.models import User, Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'content', 'view_times', 'like_times')


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(UserProfile)
