from django.contrib import admin
from ranbo.models import UserProfile
from ranbo.models import Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'view_times', 'like_times')


admin.site.register(UserProfile)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
