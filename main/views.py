from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Client
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'main/home.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            context['error'] = '账号或密码错误'
            return render(request, 'registration/login.html', context)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/login.html', context)


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

    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
        context = {}
        if form.is_valid():
            client = form.save()
            context["info"] = "注册成功"
            return render(request, 'main/register_client.html', context)
        else:
            context["info"] = "表单无效"
            return render(request, 'main/register_client.html', context)


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


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            return redirect(reverse(home))
    else:
        form = OrderForm()
    return render(request, 'order/create.html', {'form': form})


def create_position(request):
    if request.method == "POST":
        form = PermsForm(request.POST or None)
        if form.is_valid():
            perms = form.save()
            name = request.POST['name']
            Position.objects.create(perms=perms, name=name)
    else:
        form = PermsForm()
    return render(request, 'staff/position.html', {'form': form})


def staff_register(request):
    if request.method == "POST":
        form = StaffForm(request.POST or None)
        if form.is_valid():
            staff = form.save(commit=False)
            user = User.objects.create_user(username=staff.staff_id, password=request.POST.get('password'))
            staff.account = user
            staff.save()
    else:
        form = StaffForm()
    return render(request, 'registration/register.html', {'form': form})
