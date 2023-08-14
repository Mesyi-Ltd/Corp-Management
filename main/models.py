from django.contrib.auth.models import User
from django.core.validators import *
from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils.text import slugify

SCALES = [
    ("0~10", "0~10"),
    ("11~50", "11~50"),
    ("51~100", "51~100"),
    ("101~500", "101~500"),
    (">500", ">500"),
]


class Company(models.Model):
    name = models.CharField(max_length=20)
    name_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)


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
    company = models.BooleanField(default=False)
    staff_list = models.BooleanField(default=False)
    staff_detail = models.BooleanField(default=False)
    staff_create = models.BooleanField(default=False)
    staff_delete = models.BooleanField(default=False)
    staff_edit = models.BooleanField(default=False)
    staff_performance = models.BooleanField(default=False)
    item_list = models.BooleanField(default=False)
    item_create = models.BooleanField(default=False)
    item_detail = models.BooleanField(default=False)
    item_delete = models.BooleanField(default=False)
    stock_change_create = models.BooleanField(default=False)
    stock_change_list = models.BooleanField(default=False)
    self_order = models.BooleanField(default=True)


class Position(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20, default="暂定")
    perms = models.OneToOneField(Perm, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, validators=[RegexValidator('^[0-9 +]*$', message="手机号错误")])
    email = models.EmailField(null=True, blank=True)
    staff_id = models.CharField(max_length=50, error_messages={'required': '请输入工号'})
    national_id = models.CharField(max_length=18, validators=[
        MinLengthValidator(18, message="身份证格式错误"),
        RegexValidator('^[0-9a-zX]*$', message="身份证格式错误")
    ])
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[("on_post", "在职"), ("left", "离职")], default="on_post")
    employed_date = models.DateField()
    leaving_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class MonthlyPerformance(models.Model):
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='monthly')
    performance = models.FloatField(default=0)
    year = models.IntegerField(default=datetime.now().year, blank=True)
    month = models.IntegerField(default=datetime.now().month, blank=True)


class AnnualPerformance(models.Model):
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='yearly')
    performance = models.FloatField(default=0)
    year = models.IntegerField(default=datetime.now().year, blank=True)


class Client(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='client', null=True, blank=True)
    client_id = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=200)
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
    order_completed = models.IntegerField(null=True, default=0)
    registrant = models.CharField(max_length=10)
    related_staff = models.ForeignKey(Staff, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client_detail', args=(str(self.id)))


class ClientContact(models.Model):
    corp = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True)
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
    creator = models.ForeignKey(Staff, on_delete=models.PROTECT)
    method = models.CharField(max_length=10, choices=METHODS)
    content = models.FileField()
    date = models.DateField()
    next_date = models.DateField()
    next_method = models.CharField(max_length=10, choices=METHODS)
    next_plan = models.TextField()


class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('supplier_detail', kwargs={'pk': self.pk})


class SupplierContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    position = models.CharField(max_length=20)
    phonenum = models.CharField(max_length=20)
    email = models.EmailField()
    remark = models.TextField(null=True, blank=True, max_length=200)


class Item(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    item_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10, null=True, blank=True, choices=[
        ('product', '产品'),
        ('material', '原料'),
    ])
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    # unit = models.CharField(max_length=5)
    spec = models.CharField(max_length=200)
    product_type = models.CharField(max_length=6, null=True, blank=True, choices=[
        ('single', '单品'),
        ('bound', '套装')
    ])
    hair = models.CharField(max_length=30, null=True, blank=True)
    pipe = models.CharField(max_length=30, null=True, blank=True)
    handle = models.CharField(max_length=30, null=True, blank=True)
    min_order = models.IntegerField(null=True, blank=True)
    package = models.BooleanField(default=False)
    reference = models.URLField(null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        null=True
    )
    creator = models.ForeignKey(Staff, related_name='created_order', on_delete=models.PROTECT, null=True)
    staff = models.ManyToManyField(Staff, related_name='orders')
    # staff1 = models.CharField(max_length=20)
    # staff2 = models.CharField(max_length=20)
    order_num = models.CharField(max_length=20, blank=True, null=True, validators=[
        RegexValidator('^[0-9]*$', message='订单号格式错误', ),
    ])
    order_type = models.CharField(max_length=10, choices=[('normal', '大货订单'), ('sample', '样品订单')])
    production_type = models.CharField(max_length=10, choices=[('stoke', '库存'), ('produce', '生产')])
    specs = models.CharField(max_length=200)
    amount = models.IntegerField(null=True)
    ppu = models.FloatField()
    price = models.FloatField(null=True)
    deposit = models.FloatField(blank=True, null=True)
    remaining = models.FloatField(null=True, blank=True)
    address = models.TextField()
    description = models.CharField(max_length=999, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    handed = models.DateField(null=True, blank=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name="order")

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
        ('remaining_paid', '尾款已付'),
        ('checking', '质检中'),
        ('inspecting', '验货中'),
        ('shipped', '已出货'),
        ('accepted', '已确认')
    ])
    time = models.DateTimeField(auto_now_add=True)
    current = models.BooleanField(default=True, blank=True, null=True)
    creator = models.CharField(max_length=20, blank=True, null=True)


# class Image(models.Model):
#     image = models.ImageField()
#     correspondence = models.ForeignKey(on_delete=models.CASCADE, related_name='image',null=)

class OrderAttachment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True
    )
    document = models.FileField(null=False, blank=False, upload_to='file/')

    def __str__(self):
        return self.document.name.split('/')[1]


class CommunicationAttachment(models.Model):
    communication = models.ForeignKey(
        ClientCommunication, on_delete=models.CASCADE
    )
    document = models.FileField(null=False, blank=False, upload_to='file/')


class StockChange(models.Model):
    change_id = models.CharField(max_length=20, null=True, blank=True)
    source_whereabouts = models.CharField(max_length=20, null=True, blank=True)
    invoice = models.CharField(max_length=20, null=True, blank=True)
    staff = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.PROTECT)
    remark = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=[
        ('increase', '入库'),
        ('decrease', '出库')
    ])

    def get_absolute_url(self):
        return reverse('item_detail', str(self.pk))


class ItemChange(models.Model):
    stock_change = models.ForeignKey(StockChange, related_name='item', on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, related_name='change', null=True, on_delete=models.SET_NULL)
    item_name = models.CharField(max_length=20, default=item.name, blank=True)
    quantity = models.IntegerField()


class StorageChangeAttachment(models.Model):
    change = models.ForeignKey(StockChange, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/')


class Purchase(models.Model):
    purchase_id = models.CharField(max_length=20, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT, null=True)
    related_order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='purchase')

    def __str__(self):
        return self.purchase_id


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='image/', blank=True, null=True)


class PurchaseItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    purchase = models.ForeignKey(Purchase, on_delete=models.RESTRICT, related_name="purchases", blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT, related_name="purchases")
    invoice = models.CharField(max_length=20)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)
    used = models.FloatField()
    date = models.DateField()
    contract = models.FileField(upload_to='file/', )
    remark = models.CharField(max_length=200, blank=True, null=True)


class Production(models.Model):
    production_id = models.CharField(max_length=20)
    date_created = models.DateField()
    date_completed = models.DateField()
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name='production')
    staff1 = models.ForeignKey(Staff, related_name="production1", on_delete=models.RESTRICT, null=True, blank=True)
    staff2 = models.ForeignKey(Staff, related_name="production2", on_delete=models.RESTRICT, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    amount = models.IntegerField()
    unit = models.CharField(max_length=10)
    file = models.FileField(null=True, blank=True, upload_to='file/')
    status = models.CharField(null=True, blank=True, max_length=10, choices=(
        ('created', '建立'),
        ('purchasing', '原料采购'),
        ('producing', '生产'),
        ('checking', '质检'),
        ('shipping', '交货'),
        ('closed', '关闭'),
    ))
    remark = models.CharField(max_length=200, null=True, blank=True)


class QualityCheck(models.Model):
    task_id = models.CharField(max_length=20)
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT, related_name="checks")
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="checks")
    date = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.RESTRICT, related_name="checks")
    quantity = models.FloatField()
    passed = models.FloatField()
    rate = models.FloatField(validators=[MaxValueValidator(100.0), MinValueValidator(0.0)])
    remark = models.CharField(max_length=200)



