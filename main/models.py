import random

from django.contrib.auth.models import User
from django.core.validators import *
from django.db import models
from django.urls import reverse
from datetime import datetime

SCALES = [
    ("0~10", "0~10"),
    ("11~50", "11~50"),
    ("51~100", "51~100"),
    ("101~500", "101~500"),
    (">500", ">500"),
]


def rand_id(digit):
    random_id = ""
    for i in range(digit):
        random_id.join(str(random.randint))
    return random_id


class Company(models.Model):
    name = models.CharField(max_length=20)


class Perm(models.Model):
    position_all = models.BooleanField(default=False)
    order_detail = models.BooleanField(default=False)
    order_list = models.BooleanField(default=False)
    order_create = models.BooleanField(default=False)
    order_edit = models.BooleanField(default=False)
    order_delete = models.BooleanField(default=False)
    client_list = models.BooleanField(default=False)
    client_detail = models.BooleanField(default=False)
    client_edit = models.BooleanField(default=False)
    client_delete = models.BooleanField(default=False)
    client_create = models.BooleanField(default=False)
    supplier_list = models.BooleanField(default=False)
    supplier_detail = models.BooleanField(default=False)
    supplier_create = models.BooleanField(default=False)
    supplier_delete = models.BooleanField(default=False)
    supplier_edit = models.BooleanField(default=False)
    company_list = models.BooleanField(default=False)
    company_detail = models.BooleanField(default=False)
    company_create = models.BooleanField(default=False)
    company_delete = models.BooleanField(default=False)
    company_edit = models.BooleanField(default=False)
    staff_list = models.BooleanField(default=False)
    staff_detail = models.BooleanField(default=False)
    staff_create = models.BooleanField(default=False)
    staff_delete = models.BooleanField(default=False)
    staff_edit = models.BooleanField(default=False)
    staff_performance = models.BooleanField(default=False)
    self_order = models.BooleanField(default=True)


class Position(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="暂定")
    perms = models.OneToOneField(Perm, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Staff(models.Model):
    account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    staff_id = models.CharField(unique=True, max_length=50, primary_key=True)
    national_id = models.CharField(unique=True, max_length=18, validators=[
        MinLengthValidator(18, message="身份证格式错误"),
        RegexValidator('^[0-9a-zX]*$', message="身份证格式错误")
    ])
    annual_performance = models.IntegerField(default=0)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[("on_post", "在职"), ("left", "离职")])
    employed_date = models.DateField()
    leaving_date = models.DateField()

    def __str__(self):
        return self.name


class MonthlyPerformance(models.Model):
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE)
    performance = models.IntegerField()
    year = models.IntegerField(default=datetime.now().year, blank=True)


class AnnualPerformance(models.Model):
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE)
    performance = models.IntegerField()
    year = models.IntegerField(default=datetime.now().year, blank=True)
    month = models.IntegerField(default=datetime.now().month, blank=True)


class Client(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='order')
    client_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=20, choices=[
        ('assigned', '公司分配'),
        ('custom', '海关数据'),
        ('exhibition', '展会资源'),
        ('other', '其他方式')
    ])
    level = models.CharField(max_length=20, choices=[
        ('intended', '意向客户'),
        ('potential', '潜在客户'),
        ('not_intended', '无意向客户'),
        ('ordered', '下单客户')
    ])
    client_type = models.CharField(max_length=20, choices=[
        ('individual', '个人客户'),
        ('enterprise', '品牌公司'),
        ('foreign', '外贸公司'),
        ('internation', '跨境商超'),
        ('other', '其他')
    ])
    scale = models.CharField(max_length=20, choices=SCALES)
    market = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    order_in_progress = models.IntegerField(null=True, default=0)
    order_completed = models.IntegerField(null=True)
    registrant = models.CharField(max_length=10)
    related_staff = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client_detail', args=(str(self.id)))


class ClientContact(models.Model):
    corp = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女'), ('other', '其他')])
    position = models.CharField(max_length=50)
    dob = models.DateField()
    phonenum = models.CharField(max_length=20)
    email = models.EmailField()
    remark = models.TextField()


class ClientCommunication(models.Model):
    METHODS = [
        ('email', '邮件来往'),
        ('call', '电话交流'),
        ('f2f', '客户面访'),
        ('qq', 'QQ交流'),
        ('wechat', '微信交流'),
        ('other', '其他方式')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=30)
    creator = models.CharField(max_length=20)
    method = models.CharField(max_length=10, choices=METHODS)
    content = models.FileField()
    date = models.DateField()
    next_date = models.DateField()
    next_method = models.CharField(max_length=10, choices=METHODS)
    next_plan = models.TextField()


class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    commodity = models.CharField(max_length=20, null=True, choices=[
        ('brush_hair', '刷毛'),
        ('pipe', '口管'),
        ('handle', '刷柄'),
        ('production', '人工')
    ])
    scale = models.CharField(max_length=10, choices=SCALES)
    established_date = models.DateField(null=True, blank=True)
    price = models.FileField(null=True)
    invoice = models.TextField(max_length=200)
    remark = models.TextField(max_length=200)


class SupplierContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    position = models.CharField(max_length=20)
    phonenum = models.CharField(max_length=20)
    email = models.EmailField()
    remark = models.TextField(null=True, blank=True, max_length=200)


class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20)
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True
    )
    client_name = models.CharField(max_length=50, default=client.name)
    staff = models.ManyToManyField(Staff, related_name='orders')
    staff1 = models.CharField(max_length=20)
    staff2 = models.CharField(max_length=20)
    order_num = models.CharField(unique=True, primary_key=True, max_length=20, validators=[
        RegexValidator('^[0-9]*$', message='订单号格式错误')
    ])
    sample = models.ImageField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=[('stoke', '库存'), ('produce', '生产')])
    item = models.CharField(max_length=20)
    specs = models.CharField(max_length=200)
    amount = models.IntegerField(null=True)
    ppu = models.IntegerField()
    price = models.IntegerField(null=True)
    deposit = models.IntegerField()
    deposit_paid = models.DateField()
    remaining = models.IntegerField()
    remaining_paid = models.DateField()
    address = models.TextField()
    description = models.CharField(max_length=999)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    handed = models.DateField()

    def __str__(self):
        return self.order_num


#    def get_absolute_url(self):
#        return reverse('', args=(str(self.id)))


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status')
    sample_status = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('paid', '已付款'),
        ('purchasing', '原料采购'),
        ('producing', '打样中'),
        ('shipped', '已出货'),
        ('adjusting', '修样中'),
        ('accepted', '样品确认')
    ])
    status = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('paid', '定金已交'),
        ('purchasing', '原料采购'),
        ('purchased', '原料入库'),
        ('producing', '生产中'),
        ('checking', '质检中'),
        ('inspecting', '验货中'),
        ('shipped', '已出货'),
        ('accepted', '已确认')
    ])
    time = models.DateTimeField(auto_now_add=True)


# class Image(models.Model):
#     image = models.ImageField()
#     correspondence = models.ForeignKey(on_delete=models.CASCADE, related_name='image',null=)

class OrderAttachment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True
    )
    document = models.FileField(null=False, blank=False, upload_to='file/')


class CommunicationAttachment(models.Model):
    communication = models.ForeignKey(
        ClientCommunication, on_delete=models.CASCADE
    )
    document = models.FileField(null=False, blank=False, upload_to='file/')


class Item(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10, choices=[
        ('product', '产品'),
        ('material', '原料'),
    ])
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    spec = models.CharField(max_length=200)


class StorageChange(models.Model):
    change_id = models.CharField(max_length=20)
    source_whereabouts = models.CharField(max_length=20)
    invoice = models.CharField(max_length=20)
    staff = models.CharField(max_length=20)
    remark = models.TextField()


class ItemChange(models.Model):
    storage = models.ForeignKey(StorageChange, related_name='item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=20)
    item_id = models.CharField(max_length=20)
    quantity = models.IntegerField()
    type = models.CharField(max_length=10, choices=[
        ('increase', '入库'),
        ('decrease', '出库')
    ])


class StorageChangeAttachment(models.Model):
    change = models.ForeignKey(StorageChange, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/')
