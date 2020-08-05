from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import JsonResponse


def staff_required(func):
    def wrapper(request):
        if not (request.user.is_authenticated and request.user.is_superuser):
            json_res = JsonResponse({'status': 'error', 'exception': 'AuthenticateError'})
            return json_res if request.is_ajax() else redirect('main:error401')
        return func(request)
    return wrapper


def redirect_manager(request):
    return redirect('adminpanel:manager')


@staff_required
def manager(request):
    return render(request, 'adminpanel/manager.html')


def logout(request):
    auth.logout(request)
    return redirect('main:index')
