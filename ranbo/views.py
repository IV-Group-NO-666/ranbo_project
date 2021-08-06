from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ranbo.forms import *
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    thoughts = Post.objects.order_by('-like_times')[:5]
    context_dict = {'thoughts': thoughts}
    return render(request, 'ranbo/index.html', context=context_dict)


def sort_thought(request):
    thought = Post.objects.order_by('-post_id')[:5]
    if request.method == "POST":
        if 'like' in request.POST:
            thought = Post.objects.order_by('like_times')[:5]
        if 'view' in request.POST:
            thought = Post.objects.order_by('view_times')[:5]
    return render(request, 'ranbo/index.html', context=thought)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('ranbo:index'))
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'ranbo/login.html', context={'disable_login_card': True})


@login_required
def add_thought(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            return redirect('/ranbo/')
        else:
            print(form.errors)
    return render(request, 'ranbo/add_thought.html', {'form': form})


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
            return render(request, 'ranbo/index.html')

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'ranbo/register.html', context={
        'user_form': user_form,
        'profile_form': profile_form,
        'disable_login_card': True,
    })


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


def user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return render(request, 'ranbo/user_profile.html')
    thoughts = Post.objects.filter(user=user)
    total_thoughts = 0
    total_likes = 0
    total_views = 0
    for t in thoughts:
        total_thoughts += 1
        total_likes += t.like_times
        total_views += t.view_times
    context_dict = {
        'username': user.username,
        'total_thoughts': total_thoughts,
        'total_likes': total_likes,
        'total_views': total_views,
        'thoughts': thoughts,
    }
    return render(request, 'ranbo/user_profile.html', context=context_dict)


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
    return redirect(reverse('ranbo:index'))
