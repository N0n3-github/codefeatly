from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Profile
from django.http import JsonResponse
from re import match as re_match


def index(request):
    if request.method == "POST":
        response = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response['status'] = 'ok'
        else:
            response['status'] = 'error'
            response['exception'] = "Username or password is incorrect"
        return JsonResponse(response)
    return render(request, 'main/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        rank = request.POST.get('rank')
        password = request.POST.get('password')
        confirm_pwd = request.POST.get('confirm_pwd')
        response = {}
        regexes = {
            "username": r"^[A-z0-9._]{3,16}$",
            "password": r"^[A-z0-9!@#$%^&*()_ |+=;:,.?`~{}\\-]{6,40}$",
        }
        rank_options = ['Lamer',
                        'Noob',
                        'Coder',
                        'Programmer',
                        'Hacker',
                        'I hacked NASA with HTML']
        if User.objects.filter(username=username).exists():
            response['exception'] = "This username is already taken"
        elif password != confirm_pwd:
            response['exception'] = "Passwords don't match"
        elif not re_match(regexes['username'], username):
            response['exception'] = "Username did't match pattern"
        elif not re_match(regexes['password'], password):
            response['exception'] = "Password did't match pattern"
        elif rank not in rank_options:
            response['exception'] = "No such rank option found"
        if response.get('exception'):
            response['status'] = 'error'
        else:
            base_user = User.objects.create_user(username=username, password=password)
            profile = Profile(user=base_user, rank=rank)
            profile.save()
            response['status'] = 'ok'
        return JsonResponse(response)
    return render(request, 'main/signup.html')


def tasks(request):
    return render(request, 'main/tasks.html')


def logout(request):
    auth.logout(request)
    return redirect('index')
