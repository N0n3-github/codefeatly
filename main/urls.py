from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('logout/', views.logout, name="logout"),
]
