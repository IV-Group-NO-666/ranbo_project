from django.urls import path
from ranbo import views

app_name = 'ranbo'

urlpatterns = [
    path('', views.index, name='index'),
]
