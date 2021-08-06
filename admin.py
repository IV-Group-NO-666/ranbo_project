from django.contrib import admin
from ranbo.models import User, Post, like

class PostAdmin(admin.ModelAdmin):
    list_display = ('Post_id', 'Content','View_times','Like_times')

admin.site.register(User)
admin.site.register(Post,PostAdmin)
admin.site.register(like)
# Register your models here.
