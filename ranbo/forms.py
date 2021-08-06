from django import forms
from ranbo.models import User, Post, Like
from ranbo.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    username = forms.CharField(max_length=128)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


class PostForm(forms.ModelForm):
    post_id = forms.IntegerField()
    view_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    like_times = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    content = forms.TextInput()
    picture = forms.ImageField(help_text="Please enter the picture.")

    class Meta:
        model = Post
        fields = ('post_id', 'content', 'picture',)


class LikeForm(forms.ModelForm):
    like_id = forms.IntegerField()

    class Meta:
        model = Like
        fields = ('like_id',)
