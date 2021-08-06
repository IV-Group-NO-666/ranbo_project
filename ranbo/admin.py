from django.contrib import admin
from ranbo.models import UserProfile
from ranbo.models import User, Post, Like
# Register your models here.
#Authentication
admin.site.register(UserProfile)
###models
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)