from django import forms
from django.contrib.auth.models import User
from ranbo.models import User, Post, like
from ranbo.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    User_id = forms.IntegerField(widget=forms.HiddenInput())
    Username = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


class PostForm(forms.ModelForm):
    Post_id = forms.IntegerField()
    View_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    Like_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    Content = forms.TextInput()
    Picture = forms.ImageField(help_text="Please enter the picture.")

    class Meta:
        model = Post
        fields = ('post_id', 'content', 'picture',)


class LikeForm(forms.ModelForm):
    like_id = forms.IntegerField()

    class Meta:
        model = like
        fields = ('like_id',)
