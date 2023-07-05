import random

from django.contrib.auth.models import User
from django.core.validators import *
from django.db import models
from django.urls import reverse

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


class Company:
    pass


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
    account = models.OneToOneField(User, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    staff_id = models.CharField(unique=True, max_length=50, primary_key=True)
    national_id = models.CharField(unique=True, max_length=18, validators=[
        MinLengthValidator(18, message="身份证格式错误", code='invalid_length'),
        RegexValidator('^[0-9a-zX]*$', message="身份证格式错误", code='invalid_format')
    ])
    annual_performance = models.IntegerField(default=0)
    monthly_performance = models.IntegerField(default=0)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=[("on_post", "在职"), ("left", "离职")])
    employed_date = models.DateField()
    leaving_date = models.DateField()

    def __str__(self):
        return self.name


class MonthlyPerformance(models.Model):
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE)


class Client(models.Model):
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
    corp = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女'), ('other', '其他')])
    position = models.CharField(max_length=50)
    dob = models.DateField()
    phonenum = models.CharField(max_length=20)
    email = models.EmailField()
    remark = models.TextField()


class ClientCommunication(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    STATUS = [
        ("placed", "已下单"),
        ("producing", "生产中"),
        ("produced", "生产完毕"),
        ("shipping", "已发货"),
        ("delivered", "已到货"),
        ("completed", "已完成"),
    ]
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True
    )
    staff = models.ManyToManyField(Staff)
    order_num = models.IntegerField(unique=True, primary_key=True,
                                    validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    amount = models.IntegerField(null=True)
    description = models.CharField(max_length=999)
    sample = models.ImageField(null=True, blank=True)
    price = models.IntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.order_num


#    def get_absolute_url(self):
#        return reverse('', args=(str(self.id)))


class Supplier(models.Model):
    name = models.CharField(max_length=200, null=True)
    commodity = models.CharField(max_length=5, null=True, choices=[
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class SupplierContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    position = models.CharField(max_length=20)
    phonenum = models.CharField(max_length=20)
    email = models.EmailField()
    remark = models.TextField(null=True, blank=True, max_length=200)
