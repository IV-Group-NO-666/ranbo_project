from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render,get_object_or_404
from django.urls import reverse
from ranbo import models
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count,Sum


def index(request):
    thought = Thought.objects.order_by('like_times')[:5]
    # context['thought']=thought
    return render(request,'index.html',context=thought)


def sort_thought(request):
    if request.method=="POST":
        if 'time' in request.POST:
            thought = Thought.objects.order_by('time')[:5]
        if 'like' in request.POST:
            thought = Thought.objects.order_by('time')[:5]
        if 'view' in request.POST:
            thought = Thought.objects.order_by('time')[:5]
        if 'pop' in request.POST:
            thought = Thought.objects.order_by('time')[:5]
    return render(request, 'index.html', context=thought)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('rango:index'))
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html')


@login_required
def add_thought(request):
    form = ThoughtForm()
    if request.method =='POST':
        form =ThoughtForm(request.POST)
        if form.is_vaild():
            form.save(commit=True)
            return redirect('/ranbo/')
        else:
            print(form.errors)
    return render(request, 'ranbo/add_thought.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'ranbo/register.html',
                  context={'user_form': user_form, 'registered': registered})


def show_more(request):
    if request.user.is_authenticated():
        thought = thought.objects.order_by('like_times')
        return render(request, 'index.html', context=thought)
    else:
        return HttpResponse("You need to login")


def add_comment(request,thought_id):
    thought = get_object_or_404(Thought,thought_id=thought_id)
    if request.method== 'POST':
        form =commentForm(request.POST)
        if form.is_vaild():
            comment = form.save(commit=False)
            return redirect('ranbo:thought')
        else:
            return HttpResponse("fail to add comment")


def thought_detail(request,thought_id):
    context_dict = {}
    thought = Thought.objects.get(thought_id=thought_id)
    context_dict['like']=thought.like_times
    context_dict['view'] = thought.view_times
    context_dict['comment'] = thought.comment
    return render(request, 'ranbo/thought.html')


def user_info(request,user_id):
    context_dict={}
    thought = Thought.objects.get(user_id=user_id)
    total_like=thought.aggregate(Sum('like_times'))
    total_view=thought.aggregate(Sum('view_times'))
    user=User.object.get(user_id=user_id)
    context_dict['username']=user.usename
    context_dict['total_like']= total_like
    context_dict['total_view']=total_view
    return render(request,'ranbo/My-account.html')


@login_required
def like_thought(request):
    if(request.method=='GET'):
        thought_id=request.GET['thought_id']
        likes=0
        if thought_id:
            thought=Thought.objects.get(thought_id=int(thought_id))
            if thought:
                likes=thought.like_times+1
                thought.like_times=likes
                thought.save()
        return HttpResponse(likes)


def user_edit(request):
    user=User.object.get(user_id=request.user.user_id)
    if request.method=='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user.username=user_form.cleaned_data['username']
            user.password=user_form.cleaned_data['password']
            user.save()
        return HttpResponseRedirect('/ranbo/My-account/')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


