from django.db import models
from django.contrib.auth.models import User


# Authentication
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_times = models.IntegerField(default=0)
    like_times = models.IntegerField(default=0)
    content = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return str(self.user)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_id = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return str(self.user)
