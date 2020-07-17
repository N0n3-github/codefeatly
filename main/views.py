from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def signup(request):
    return render(request, 'main/signup.html')
