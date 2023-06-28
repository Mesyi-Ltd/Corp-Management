from django.shortcuts import render
from .forms import *
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Client
from django.contrib.auth import login, logout


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

    # def post(self, request, *args, **kwargs):
    #     form = ClientForm(request.POST)
    #     context = {}
    #     if form.is_valid():
    #         client = form.save()
    #         context["info"] = "注册成功"
    #         return render(request, 'main/register_client.html', context)
    #     else:
    #         return render(request)


#    fields = '__all__'

class ClientList(ListView):
    model = Client
    template_name = 'main/client_list.html'


class ClientDetail(DetailView):
    model = Client
    template_name = 'main/client_detail.html'


class SupplierList(ListView):
    model = Supplier
    template_name = 'main/supplier_list.html'


class SupplierDetail(DetailView):
    model = Supplier
    template_name = 'main/supplier_detail.html'
