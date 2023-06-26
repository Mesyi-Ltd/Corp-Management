from django.shortcuts import render


def home(request):
    return render(request, 'main/home.html')


def login_page(request):
    return render(request, 'main/login.html')


def performance(request):
    return render(request, 'main/performance.html')
