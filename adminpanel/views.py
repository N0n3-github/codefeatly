from django.shortcuts import render, redirect
from django.contrib.auth.models import auth


def manager(request):
    return render(request, 'adminpanel/manager.html')


def logout(request):
    auth.logout(request)
    return redirect('main:index')
