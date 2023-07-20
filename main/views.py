import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from Corp_Management.settings import MEDIA_ROOT
from .forms import *
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Client
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def rand_id(digit):
    random_id = ""
    for i in range(digit):
        random_id += str(random.randint(0, 9))
    return random_id


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
    return render(request, 'staff/performance.html')


def register_company(request):
    form = ClientForm
    context = {'form': form}
    return render(request, 'client/register_client.html', context)


class RegisterClient(CreateView):
    model = Client
    template_name = 'client/register_client.html'
    form_class = ClientForm

    # def post(self, request, *args, **kwargs):
    #     form = ClientForm(request.POST)
    #     context = {}
    #     if form.is_valid():
    #         client = form.save()
    #         context["info"] = "注册成功"
    #         return render(request, 'client/register_client.html', context)
    #     else:
    #         context["info"] = "表单无效"
    #         return render(request, 'client/register_client.html', context)


#    fields = '__all__'

class ClientList(ListView):
    model = Client
    template_name = 'client/client_list.html'
    # for client in Client.objects.all():
    #     orders = client.order_set.all()
    #     for order in orders:
    #         order.status.all().


class ClientDetail(DetailView):
    model = Client
    template_name = 'client/client_detail.html'


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
            order = form.save(commit=False)
            order.client_name = order.client.name
            random_id = rand_id(10)
            while Order.objects.filter(order_num=random_id).exists():
                random_id = rand_id(10)
            order.order_num = random_id
            order.remaining = order.price - order.deposit
            order.save()
            form.save_m2m()
            order.client.order_in_progress = Order.objects.filter(client=order.client, completed=False).count()
            order.client.save()
            for file in request.FILES.getlist('files'):
                OrderAttachment.objects.create(order=order, document=file)
            return redirect('order_detail', order.pk)
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
            user = User.objects.create_user(
                username=staff.staff_id,
                password=request.POST.get('password'),
                email=request.POST.get('email')
            )
            staff.account = user
            staff.save()
            messages.success(request, f'成功创建员工 {staff}')
            return redirect('staff_detail', pk=staff.staff_id)
    else:
        form = StaffForm()
    return render(request, 'registration/register.html', {'form': form})


class StaffDetail(DetailView):
    model = Staff
    template_name = 'staff/detail.html'


class StaffList(ListView):
    model = Staff
    template_name = 'staff/list.html'


def staff_edit(request, pk):
    staff = Staff.objects.get(staff_id=pk)
    form = StaffUpdateForm(request.POST or None, instance=staff)
    if form.is_valid() and request.method == 'POST':
        form.save()
        if staff.status == 'left':
            staff.account.is_active = False
            staff.account.save()
        return redirect('staff_detail', pk)
    return render(request, 'staff/edit.html', {'form': form, 'id': staff.staff_id})


class AddItem(CreateView):
    form_class = AddItem
    model = Item
    template_name = 'item/add.html'

    def get_success_url(self):
        return reverse('item_detail', kwargs={'pk': self.object.pk})


class ItemDetail(DetailView):
    model = Item
    template_name = 'item/detail.html'


class OrderList(ListView):
    model = Order
    template_name = 'order/list.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     if OrderStatus.objects.filter(order=order, current=True).exists():
    #         context['current'] = order.status.get(current=True, order=order)


class OrderDetail(DetailView):
    model = Order
    template_name = 'order/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        order = self.get_object()
        context['staff'] = order.staff.all()
        if order.order_type == 'normal':
            context['type'] = 'normal'
            form = NormalStatus()
        else:
            form = SampleStatus()
            context['type'] = 'sample'

        if order.completed:
            context['completed'] = 'True'
        context['form'] = form

        if order.status.all().filter(current=True).exists():
            context['current'] = order.status.get(current=True)

        context['status_history'] = order.status.all()
        context['attachments'] = OrderAttachment.objects.filter(order=order)
        return context

    def post(self, *args, **kwargs):
        order = self.get_object()
        if order.order_type == 'normal':
            form = NormalStatus(self.request.POST or None)
        else:
            form = SampleStatus(self.request.POST or None)

        if form.is_valid():
            OrderStatus.objects.filter(order=order).update(current=False)
            status = form.save(commit=False)
            status.order = order
            status.creator = self.request.user.staff.name
            status.save()
            if status.status == 'accepted' or status.sample_status == 'accepted':
                order.completed = True
                order.save()
                order.client.order_in_progress = Order.objects.filter(client=order.client, completed=False).count()
                order.client.save()
            return redirect('order_detail', order.pk)

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


def order_download(request, pk):
    file = OrderAttachment.objects.get(id=pk)
    return FileResponse(open(MEDIA_ROOT+'/'+file.document.name, 'rb'), as_attachment=True)
