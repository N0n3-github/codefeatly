from django.shortcuts import render, redirect
from django.contrib.auth.models import auth


def redirect_manager(request):
    return redirect('adminpanel:manager')


def manager(request):
    if request.path == '/adminpanel/':
        return redirect('adminpanel:manager')
    return render(request, 'adminpanel/manager.html')


def logout(request):
    auth.logout(request)
    return redirect('main:index')
