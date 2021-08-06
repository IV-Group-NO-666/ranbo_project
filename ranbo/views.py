from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from ranbo.models import *
from ranbo.forms import *


def index(request):
    thoughts = Post.objects.order_by('like_times')[:5]
    context_dict = {'thoughts': thoughts}
    return render(request, 'ranbo/index.html', context=context_dict)


def sort_thought(request):
    thought = Post.objects.order_by('post_id')[:5]
    if request.method == "POST":
        if 'like' in request.POST:
            thought = Post.objects.order_by('like_times')[:5]
        if 'view' in request.POST:
            thought = Post.objects.order_by('view_times')[:5]
    return render(request, 'ranbo/index.html', context=thought)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('rango:index'))
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'ranbo/login.html')


@login_required
def add_thought(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_vaild():
            form.save(commit=True)
            return redirect('/ranbo/')
        else:
            print(form.errors)
    return render(request, 'ranbo/add_post.html', {'form': form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'ranbo/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def show_more(request):
    if request.user.is_authenticated():
        thought = Post.objects.order_by('like_times')
        return render(request, 'ranbo/index.html', context=thought)
    else:
        return HttpResponse("You need to login")


# def add_comment(request, post_id):
#     thought = get_object_or_404(Post, Post_id=post_id)
#     if request.method == 'POST':
#         form = commentForm(request.POST)
#         if form.is_vaild():
#             comment = form.save(commit=False)
#             return redirect('ranbo:thought')
#         else:
#             return HttpResponse("fail to add comment")


def thought_detail(request, post_id):
    context_dict = {}
    thought = Post.objects.get(post_id=post_id)
    context_dict['like'] = thought.like_times
    context_dict['view'] = thought.view_times
    context_dict['comment'] = thought.comment
    return render(request, 'ranbo/thought_detail.html')


def user_info(request, user_id):
    context_dict = {}
    thought = Post.objects.get(user_id=user_id)
    total_like = thought.aggregate(Sum('like_times'))
    total_view = thought.aggregate(Sum('view_times'))
    user = User.object.get(User_id=user_id)
    context_dict['username'] = user.usename
    context_dict['total_like'] = total_like
    context_dict['total_view'] = total_view
    return render(request, 'ranbo/user_profile.html')


@login_required
def like_thought(request):
    if request.method == 'GET':
        thought_id = request.GET['post_id']
        likes = 0
        if thought_id:
            thought = Post.objects.get(post_id=int(thought_id))
            if thought:
                likes = thought.like_times + 1
                thought.like_times = likes
                thought.save()
        return HttpResponse(likes)


def user_edit(request):
    user = User.object.get(user_id=request.user.user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user.username = user_form.cleaned_data['username']
            user.password = user_form.cleaned_data['password']
            user.save()
        return HttpResponseRedirect('/ranbo/user_profile/')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
