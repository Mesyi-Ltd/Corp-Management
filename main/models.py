import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


def rand_id(digit):
    random_id = ""
    for i in range(digit):
        random_id.join(str(random.randint))
    return random_id


class Perm(models.Model):
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


class Position(models.Model):
    name = models.CharField(max_length=200, default="暂定")
    perms = models.OneToOneField(Perm, on_delete=models.CASCADE)


class Staff(models.Model):
    POSITION = [
        ("manager", "经理"),
        ("salesman", "业务员"),
        ("order_admin", "跟单员"),
        ("purchaser", "采购员"),
        ("warehouse_admin", "仓管员"),
        ("production_admin", "生产管理员")
    ]
    name = models.CharField(max_length=200)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    staff_id = models.CharField(unique=True, max_length=50, primary_key=True)
    total_performance = models.IntegerField(default=0)
    monthly_performance = models.IntegerField(default=0)
    position = models.CharField(max_length=200, null=True, choices=POSITION)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    order_in_progress = models.IntegerField(null=True, default=0)
    credible = models.BooleanField(
        default=True,
    )
    order_placed = models.IntegerField(null=True)
    order_completed = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client_detail', args=(str(self.id)))


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
    id = models.IntegerField(unique=True, primary_key=True,
                             validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    amount = models.IntegerField(null=True)
    description = models.CharField(max_length=999)
    sample = models.ImageField(null=True, blank=True)
    price = models.IntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.id


#    def get_absolute_url(self):
#        return reverse('', args=(str(self.id)))


class Supplier(models.Model):
    name = models.CharField(max_length=200, null=True)
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=200)
    commodity = models.CharField(max_length=200, null=True, default="待输入")
    price = models.IntegerField(null=True)
