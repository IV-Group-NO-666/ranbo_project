from django.urls import path
from ranbo import views

app_name = 'ranbo'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('thoughts/add-thought/', views.add_thought, name='add_thought'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
]
