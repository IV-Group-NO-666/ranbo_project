from django.db import models


class User(models.Model):
    user_id = models.IntegerField(default=0, unique=True)
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return str(self.user_id)


# Authentication
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.IntegerField(default=0, unique=True)
    view_times = models.IntegerField(default=0)
    like_times = models.IntegerField(default=0)
    content = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return str(self.post_id)


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_id = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return str(self.user_id)
