import datetime
import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from Corp_Management.settings import MEDIA_ROOT
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from .models import Client
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .decorators import allowed_users


def rand_id(digit):
    random_id = ""
    for i in range(digit):
        random_id += str(random.randint(0, 9))
    return random_id


@login_required(login_url='login')
def home(request):
    return render(request, 'main/home.html')


@login_required(login_url='login')
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


@login_required(login_url='login')
@allowed_users(["company_create"])
def register_company(request):
    form = ClientForm
    context = {'form': form}
    return render(request, 'client/register_client.html', context)


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator(allowed_users(["client_create"]), name="dispatch")
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

@login_required(login_url='login')
@allowed_users(["client_create"])
def register_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST or None)
        if form.is_valid():
            client = form.save(commit=False)
            now = datetime.now()
            day, month = str(now.day), str(now.month)
            if now.month < 10:
                month = '0' + str(now.month)
            if now.day < 10:
                day = '0' + str(now.day)
            c_id = str(now.year) + month + day + rand_id(6)
            while c_id in Client.objects.values_list('client_id', flat=True):
                c_id = str(now.year) + month + day + rand_id(6)
            client.client_id = c_id
            client.save()
            return redirect('client_detail', client.pk)
    else:
        form = ClientForm()
    return render(request, 'client/register_client.html', {'form': form})


@method_decorator([login_required(login_url='login')], name="dispatch")
@method_decorator([allowed_users(["client_list"])], name="dispatch")
class ClientList(ListView):
    paginate_by = 15
    model = Client
    template_name = 'client/client_list.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(client_id__contains=search) | Q(name__contains=search)).distinct()
        qs = qs.order_by('-order_in_progress')
        return qs

    def get_context_data(self, **kwargs):
        context = super(ClientList, self).get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['query'] = query
        return context


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["client_detail"])], name="dispatch")
class ClientDetail(DetailView):
    model = Client
    template_name = 'client/client_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        client = self.get_object()
        context['client'] = client
        context['orders'] = Order.objects.filter(client=client)
        context['current_orders'] = Order.objects.filter(client=client, completed=False)
        return context


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["supplier_list"])], name="dispatch")
class SupplierList(ListView):
    model = Supplier
    template_name = 'supplier/supplier_list.html'


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["supplier_detail"])], name="dispatch")
class SupplierDetail(DetailView):
    model = Supplier
    template_name = 'supplier/supplier_detail.html'


@login_required(login_url='login')
@allowed_users(["order_create"])
def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_name = order.client.name
            random_id = rand_id(10)
            while Order.objects.filter(order_num=random_id).exists():
                random_id = rand_id(10)
            if order.order_type == 'normal':
                order.order_num = '10' + random_id
            else:
                order.order_num = '12' + random_id
            order.remaining = order.price - order.deposit
            order.creator = request.user.staff
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


@login_required(login_url='login')
@allowed_users(["position_all"])
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


@login_required(login_url='login')
@allowed_users(["staff_create"])
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
            monthly = MonthlyPerformance.objects.create(owner=staff)
            yearly = AnnualPerformance.objects.create(owner=staff)
            monthly.save()
            yearly.save()
            messages.success(request, f'成功创建员工 {staff}')
            return redirect('staff_detail', pk=staff.staff_id)
    else:
        form = StaffForm()
    return render(request, 'registration/register.html', {'form': form})


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["staff_detail"])], name="dispatch")
class StaffDetail(DetailView):
    model = Staff
    template_name = 'staff/detail.html'

    def post(self, request, *args, **kwargs):
        password1 = self.request.POST.get('password1', '')
        password2 = self.request.POST.get('password2', '')
        if password2 == password1:
            user = self.get_object().account
            user.set_password(password1)
            user.save()
            messages.success(request, '密码已更改')
            if request.user == user:
                logout(request)
        else:
            messages.warning(request, '两次密码不一致')
        return redirect('staff_detail', self.get_object().pk)


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["staff_list"])], name="dispatch")
class StaffList(ListView):
    paginate_by = 15
    model = Staff
    template_name = 'staff/list.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(staff_id__contains=search) | Q(name__contains=search) | Q(phone__contains=search)).distinct()
        qs = qs.order_by('-status')
        return qs

    def get_context_data(self, **kwargs):
        context = super(StaffList, self).get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['query'] = query
        return context


@login_required(login_url='login')
@method_decorator([allowed_users(["staff_edit"])], name="dispatch")
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


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator(allowed_users(["item_create"]), name="dispatch")
class AddItem(CreateView):
    form_class = AddItemForm
    model = Item
    template_name = 'item/add.html'

    def post(self, request, *args, **kwargs):
        form = AddItemForm(request.POST or None)
        if form.is_valid():
            item = form.save()
            for image in request.FILES.getlist('images'):
                ItemImage.objects.create(item=item, image=image)
            return redirect('item_detail', item.pk)

    def get_success_url(self):
        return reverse('item_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator(allowed_users(["item_detail"]), name="dispatch")
class ItemDetail(DetailView):
    model = Item
    template_name = 'item/detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['images'] = ItemImage.objects.filter(item=self.get_object())
        context['item'] = self.get_object()
        return context


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["order_list"])], name="dispatch")
class OrderList(ListView):
    paginate_by = 15
    model = Order
    template_name = 'order/list.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(order_num__contains=search) | Q(client__name__contains=search) | Q(item__name__contains=search) | Q(
                    staff__name__contains=search)).distinct()
        qs = qs.order_by('-created')
        return qs

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['query'] = query
        return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     if OrderStatus.objects.filter(order=order, current=True).exists():
    #         context['current'] = order.status.get(current=True, order=order)


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["order_detail"])], name="dispatch")
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
                yearly, monthly = AnnualPerformance.objects.get(owner=order.creator, current=True), \
                    MonthlyPerformance.objects.get(owner=order.creator, current=True)
                yearly.performance += order.price
                monthly.performance += order.price
                yearly.save()
                monthly.save()
            return redirect('order_detail', order.pk)

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


@login_required(login_url='login')
@method_decorator([allowed_users(["order_detail"])], name="dispatch")
def order_download(request, pk):
    file = OrderAttachment.objects.get(id=pk)
    return FileResponse(open(MEDIA_ROOT + '/' + file.document.name, 'rb'), as_attachment=True)


@method_decorator(login_required(login_url='login'), name="dispatch")
@method_decorator([allowed_users(["item_list"])], name="dispatch")
class ItemList(ListView):
    paginate_by = 15
    model = Item
    template_name = 'item/list.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(item_id__contains=search) | Q(name__contains=search)).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            context['query'] = query
        return context


@login_required(login_url='login')
@allowed_users(["stock_change_create"])
def storage_change(request):
    change = StockChange.objects.create()
    change.save()
    return redirect('storage_change', change.pk)


@login_required(login_url='login')
@allowed_users(["stock_change_create"])
def update_storage_change(request, pk):
    change = StockChange.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateStorage(request.POST, instance=change)
        if form.is_valid():
            form.save()
            return redirect('change_detail', pk)
    else:
        form = UpdateStorage(instance=change)

    context = {'form': form}
    return render(request, 'storage/create_storage_change.html', context=context)


@login_required(login_url='login')
@allowed_users(["stock_change_create"])
def change_detail(request, pk):
    change = StockChange.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = ItemChangeForm(request.POST or None)
        if form.is_valid():
            item_change = form.save(commit=False)
            item_change.stock_change = change
            item_change.item_name = item_change.item.name
            item_change.save()
        else:
            messages.error(request, '表单无效, 请重新填写')
    else:
        form = ItemChangeForm()
    context['change'] = change
    context['form'] = form
    context['item_changes'] = ItemChange.objects.filter(stock_change=change).order_by('-pk')
    return render(request, 'storage/change_detail.html', context=context)


@login_required(login_url='login')
@allowed_users(["stock_change_create"])
def change_complete(request, pk):
    change = StockChange.objects.get(pk=pk)
    if not change.completed:
        item_changes = ItemChange.objects.filter(stock_change=change)
        for item_change in item_changes:
            item = item_change.item
            if change.type == 'increase':
                item.amount += item_change.quantity
            else:
                item.amount -= item_change.quantity
            item.save()
        change.completed = True
        change.save()
        messages.success(request, '添加成功')
    else:
        messages.warning(request, '数目已成功添加进库存，请勿重复操作')
    return redirect('change_detail', pk)


@login_required(login_url='login')
@allowed_users(["staff_performance"])
def annual_performance(request):
    context = {}
    context['selected_year'] = datetime.now().year
    context['years'] = AnnualPerformance.objects.values_list('year', flat=True).distinct()
    context['performances'] = AnnualPerformance.objects.filter(year=datetime.now().year)
    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        context['selected_year'] = selected_year
        context['performances'] = AnnualPerformance.objects.filter(year=selected_year)

    return render(request, 'performance/annual_performance.html', context=context)


@login_required(login_url='login')
@allowed_users(["staff_performance"])
def monthly_performance(request):
    context = {}
    context['selected_year'], context['selected_month'] = datetime.now().year, datetime.now().month
    context['years'] = MonthlyPerformance.objects.values_list('year', flat=True).distinct()
    context['month'] = MonthlyPerformance.objects.filter(year=datetime.now().year).values_list('month',
                                                                                               flat=True).distinct()
    context['performances'] = MonthlyPerformance.objects.filter(year=datetime.now().year, month=datetime.now().month)
    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        context['selected_year'] = selected_year
        context['month'] = MonthlyPerformance.objects.filter(year=selected_year).values_list('month',
                                                                                             flat=True).distinct()
        if request.POST.get('month'):
            selected_month = int(request.POST.get('month'))
            context['performances'] = MonthlyPerformance.objects.filter(year=selected_year, month=selected_month)
            context['selected_month'] = selected_month
    return render(request, 'performance/monthly_performance.html', context=context)


@login_required(login_url='login')
@allowed_users(["stock_change_create"])
def delete_item_change(request, pk):
    change = ItemChange.objects.get(pk=pk)
    stock_pk = change.stock_change.pk
    change.delete()
    messages.success(request, '删除成功')
    return redirect('change_detail', stock_pk)


@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator([allowed_users(["supplier_create"])], name="dispatch")
class CreateSupplier(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "supplier/supplier_create.html"


@login_required(login_url='login')
@allowed_users(["supplier_detail"])
def price_download(request, pk):
    filename = Supplier.objects.get(id=pk).price.name.split('/')[-1]
    return FileResponse(open(MEDIA_ROOT + '/' + filename, 'rb'), as_attachment=True)


def add_purchase(request, pk):
    order = Order.objects.get(pk=pk)
    purchase = Purchase.objects.create(related_order=order)
    purchase.save()
    return redirect('purchase_edit', pk=pk)


def edit_purchase(request, pk):
    purchase = Order.objects.get(pk=pk).purchase
    if request.method == "POST":
        form = PurchaseForm(request.POST or None, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('purchase_detail', pk=pk)
        else:
            messages.error(request, "表单无效")
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'purchase/edit.html', {'form': form})


def purchase_detail(request, pk):
    purchase = Order.objects.get(pk=pk).purchase
    purchase_list = PurchaseItem.objects.filter(purchase=purchase)
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST or None)
        if form.is_valid():
            item = form.save(commit=False)
            item.purchase = purchase
            item.save()
        else:
            messages.error(request, '表单无效')
    else:
        form = PurchaseItemForm()
    return render(request, 'purchase/detail.html', {'form': form, 'purchase': purchase, 'purchase_list': purchase_list})


