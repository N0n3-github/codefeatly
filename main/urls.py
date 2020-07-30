from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('tasks', views.tasks, name="tasks"),
    path('logout', views.logout, name="logout"),
]
