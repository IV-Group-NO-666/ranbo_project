from django import forms
from django.contrib.auth.models import User
from ranbo.models import UserProfile, Post, Like


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


class PostForm(forms.ModelForm):
    content = forms.CharField(max_length=200)
    # picture = forms.ImageField(widget=forms.HiddenInput(), help_text="Please enter the picture.")
    # view_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # like_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Post
        fields = ('content',)


class LikeForm(forms.ModelForm):
    like_id = forms.IntegerField()

    class Meta:
        model = Like
        fields = ('like_id',)
