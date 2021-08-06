from django import forms
#from ranbo.models import Page, Category
from django.contrib.auth.models import User
from ranbo.models import User, Post, like
from ranbo.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    User_id = forms.IntegerField()
    Username = forms.CharField(max_length=128)
    class Meta:
        model = User
        fields = ('User_id','Username', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',) 
        
class PostForm(forms.ModelForm):
    Post_id = forms.IntegerField()
    View_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    Like_times =forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    Content = forms.TextField(help_text="Please enter the content.")
    Picture = forms.ImageField(blank=True,help_text="Please enter the picture.")
    class Meta:
        model = Post
        fields = ('Post_id','Content', 'Picture',)

class likeForm(forms.ModelForm):
    like_id = forms.IntegerField(default=0,unique=True)
    class Meta:
        model = like
        fields = ('like_id')
