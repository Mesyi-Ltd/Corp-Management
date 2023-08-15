from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    # credible = forms.BooleanField(
    #     required=False,
    # )

    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address',
                  'country', 'source', 'level', 'scale', 'client_type', 'market')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'scale': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'client_type': forms.Select(attrs={'class': 'form-select'}),
            'market': forms.TextInput(attrs={'class': 'form-control'}),

        }

        labels = {
            'name': '名称',
            'email': '电子邮箱',
            'phone': '联系电话',
            'address': '地址',
            'country': '所在国家/地区',
            'source': '客户来源',
            'scale': '规模',
            'level': '客户等级',
            'client_type': '客户类型',
            'market': '所属市场'

        }


class OrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-select', }),
                                    label='客户')
    staff = forms.ModelMultipleChoiceField(queryset=Staff.objects.all(),
                                           widget=forms.SelectMultiple(attrs={'class': 'form-select', }),
                                           label='相关员工', )
    item = forms.ModelChoiceField(queryset=Item.objects.filter(type='product'),
                                  widget=forms.Select(attrs={'class': 'form-select', }),
                                  label='产品名称')

    class Meta:
        model = Order
        fields = ['client', 'staff', 'order_type', 'item', 'specs', 'production_type',
                  'address', 'amount', 'ppu', 'price', 'deposit', 'description']

        widgets = {
            # 'order_num': forms.TextInput(attrs={'class': 'form-control', }),
            'order_type': forms.Select(attrs={'class': 'form-control', }),
            'item': forms.Select(attrs={'class': 'form-control', }),
            'production_type': forms.Select(attrs={'class': 'form-control'}),
            'specs': forms.TextInput(attrs={'class': 'form-control', }),
            'amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'ppu': forms.NumberInput(attrs={'class': 'form-control', }),
            'price': forms.NumberInput(attrs={'class': 'form-control', }),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', }),
            'description': forms.Textarea(attrs={'class': 'form-control'}, ),
            'address': forms.Textarea(attrs={'class': 'form-control', }),
            # 'handed': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'})
        }

        labels = {
            # 'order_num': '订单号',
            'client': '客户',
            'staff': '相关员工',
            'order_type': '订单类型',
            'production_type': '货物类型',
            'item': '商品名称',
            'specs': '规格型号',
            'amount': '订购数量',
            'ppu': '商品单价',
            'price': '商品总价',
            'deposit': '定金',
            'description': '备注',
            'address': '收货地址',
        }


class StaffForm(forms.ModelForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-select', }),
                                      label='职位')

    class Meta:
        model = Staff
        fields = ['staff_id', 'name', 'phone', 'email', 'national_id', 'position', 'employed_date']

        widgets = {
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'employed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        labels = {
            'staff_id': '工号',
            'name': '姓名',
            'phone': '手机号',
            'email': '邮箱',
            'national_id': '身份证号',
            'employed_date': '入职日期'
        }


class PermsForm(forms.ModelForm):
    class Meta:
        model = Perm
        fields = '__all__'

        labels = {
            'position_all': '职位全部 ',
            'self_order': '个人订单',
            'order_detail': '订单详情 ',
            'order_list': '订单列表',
            'order_create': '创建订单 ',
            'order_edit': '编辑订单',
            'order_delete': '删除订单 ',
            'client_list': '客户列表',
            'client_edit': '编辑客户',
            'client_create': '创建客户',
            'client_delete': '删除客户',
            'client_detail': '客户信息',
            'supplier_delete': '供应商列表',
            'supplier_detail': '供应商信息',
            'supplier_create': '创建供应商',
            'supplier_list': '供应商列表',
            'supplier_edit': '编辑供应商',
            'company': '公司权限',
            'staff_edit': '编辑员工',
            'staff_create': '创建员工',
            'staff_detail': '员工信息',
            'staff_delete': '删除员工',
            'staff_list': '员工列表',
            'staff_performance': '员工业绩',
            'item_detail': '产品详情',
            'item_list': '产品列表',
            'item_create': '创建产品',
            'item_delete': '删除产品',
            'stock_change_list': '入库/出库列表',
            'stock_change_create': '登记入库/出库'
        }

    def __init__(self, *args, **kwargs):
        super(PermsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-check-input checkboxes'
            field.widget.attrs['type'] = 'checkbox'
            field.widget.attrs['role'] = 'switch'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']

        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'phone', 'email', 'national_id',
                  'position', 'status', 'employed_date', 'leaving_date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'employed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'leaving_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        labels = {
            'name': '姓名',
            'phone': '手机号',
            'email': '电子邮箱',
            'national_id': '身份证号',
            'position': '职位',
            'status': '员工状态',
            'employed_date': '入职日期',
            'leaving_date': '离职日期',
        }


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('company', )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_id': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'spec': forms.Textarea(attrs={'class': 'form-control'}),
            'hair': forms.TextInput(attrs={'class': 'form-control'}),
            'pipe': forms.TextInput(attrs={'class': 'form-control'}),
            'handle': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': '名称',
            'item_id': '编号',
            'type': '类型',
            'amount': '库存',
            'spec': '规格',
            'hair': '刷毛',
            'pipe': '口管',
            'handle': '刷柄',
            'min_order': '起定量',
            'reference': '参考链接',
            'remark': '备注',
            'product_type': '产品类型',
            'package': '收纳'
        }


class NormalStatus(forms.ModelForm):
    class Meta:
        model = OrderStatus
        fields = ['status']

        widgets = {'status': forms.Select(attrs={'required': 'True'})}

        labels = {
            'status': '更新状态'
        }


class SampleStatus(forms.ModelForm):
    class Meta:
        model = OrderStatus
        fields = ['sample_status']

        widgets = {'sample_status': forms.Select(attrs={'required': 'True'})}

        labels = {'sample_status': '更新状态'}


class UpdateStorage(forms.ModelForm):
    staff = forms.ModelChoiceField(queryset=Staff.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-select', }),
                                   label='相关员工', )

    class Meta:
        model = StockChange

        fields = ['change_id', 'source_whereabouts', 'invoice', 'type', 'staff', 'remark', 'date']

        widgets = {
            'change_id': forms.TextInput(attrs={'class': 'text-input', 'required': 'true'}),
            'source_whereabouts': forms.TextInput(attrs={'class': 'text-input', 'required': ''}),
            'invoice': forms.TextInput(attrs={'class': 'text-input', 'required': ''}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'required': ''}),
            'date': forms.DateInput(attrs={'class': 'date', 'type': 'date'}, format='%Y/%m/%d'),
            'type': forms.Select()
        }
        labels = {
            'change_id': '编号',
            'source_whereabouts': '来源/去向',
            'invoice': '单据编号'
        }

    # def __init__(self, *args, **kwargs):
    #     super(UpdateStorage, self).__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.label = ""


class ItemChangeForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-select', }),
                                  label='物品')

    class Meta:
        model = ItemChange

        fields = ['item', 'quantity']

        widgets = {'quantity': forms.NumberInput(attrs={'class': 'text-input'})}

        labels = {'quantity': '数量'}


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ('company', )

        widgets = {'established_date': forms.DateInput(attrs={'type': 'date'})}


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        exclude = ('related_order', )

        labels = {
            'purchase_id': '采购编号',
            'staff': '采购员工'
        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        exclude = ('purchase', )

        widgets = {'date': forms.DateInput(attrs={'type': 'date'},)}
        labels = {
            'item': '物品',
            'supplier': '供应商',
            'invoice': '单据编号',
            'quantity': '数量',
            'unit': '单位',
            'used': '预计用量',
            'date': '需求日期',
            'contract': '合同附件',
            'remark': '备注'

        }


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        exclude = ('order', )

        widgets = {'date_created': forms.DateInput(attrs={'type': 'date'}),
                   'date_completed': forms.DateInput(attrs={'type': 'date'})}

        labels = {
            'production_id': '编号',
            'date_created': '下单日期',
            'date_completed': '交货日期',
            'staff1': '跟单员',
            'staff2': '业务员',
            'item': '产品',
            'amount': '数量',
            'unit': '单位',
            'status': '生产状态',
            'file': '附件',
            'remark': '备注'
        }


class QualityCheckForm(forms.ModelForm):
    class Meta:
        model = QualityCheck
        exclude = ('order', 'rate', )

        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

        labels = {
            'task_id': '任务编号',
            'staff': '质检员',
            'date': '质检日期',
            'item': '产品',
            'quantity': '质检数量',
            'passed': '合格数',
            'remark': '备注',
        }
