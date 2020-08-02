from django.urls import path
from . import views

app_name = "adminpanel"
urlpatterns = [
    path('manager', views.manager, name="manager"),
    path('logout/', views.logout, name="logout"),
]
