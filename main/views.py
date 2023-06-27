from django.shortcuts import render
from .forms import *
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .models import Client


def home(request):
    return render(request, 'main/home.html')


def login_page(request):
    return render(request, 'main/login.html')


def performance(request):
    return render(request, 'main/performance.html')


def register_company(request):
    form = ClientForm
    context = {'form': form}
    return render(request, 'main/register_client.html', context)


class RegisterClient(CreateView):
    model = Client
    template_name = 'main/register_client.html'
    form_class = ClientForm
#    fields = '__all__'
