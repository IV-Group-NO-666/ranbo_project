from django.urls import path
from ranbo import views

app_name = 'ranbo'

urlpatterns = [
    path('', views.index, name='index'),
    path('thought/<user_id>/add-post',views.add_thought, name='add_thought')
]
