from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Authentication
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
def __str__(self):
    return self.user.username

###models
class User(models.Model):
    User_id = models.IntegerField(default=0,unique=True)
    Username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self): 
        return self.User_id

class Post(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Post_id = models.IntegerField(default=0,unique=True)
    View_times = models.IntegerField(default=0)
    Like_times = models.IntegerField(default=0)
    Content = models.TextField()
    Picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self): 
        return self.Post_id


class like(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_id = models.IntegerField(default=0,unique=True)

    def __str__(self): 
        return self.User_id
