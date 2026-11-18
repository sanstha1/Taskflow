from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/',views.task_detail, name='task-detail'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout')
]
