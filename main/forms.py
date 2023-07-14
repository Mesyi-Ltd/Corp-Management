from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    # credible = forms.BooleanField(
    #     required=False,
    # )

    class Meta:
        model = Client
        fields = ('client_id', 'name', 'email', 'phone', 'address',
                  'country', 'source', 'level', 'scale', 'client_type', 'market')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),

        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_num', 'client', 'staff', 'type', 'item', 'specs',
                  'address', 'amount', 'ppu', 'price', 'deposit', 'description']

        widgets = {
            'order_num': forms.TextInput(attrs={'class': 'form-control', }),
            'client': forms.ModelChoiceField(queryset=Client.objects.all(), attrs={'class': 'form-control', }),
            'staff': forms.ModelMultipleChoiceField(queryset=Staff.objects.all(),
                                                    attrs={'class': 'form-control', 'size': 2}),
            'type': forms.TextInput(attrs={'class': 'form-control', }),
            'item': forms.Select(attrs={'class': 'form-control', }),
            'specs': forms.TextInput(attrs={'class': 'form-control', }),
            'amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'ppu': forms.NumberInput(attrs={'class': 'form-control', }),
            'price': forms.NumberInput(attrs={'class': 'form-control', }),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control'},),
            'address': forms.TextInput(attrs={'class': 'form-control', }),
            # 'handed': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'})
        }

        labels = {
            'order_num': '订单号',
            'client': '客户',
            'staff': '相关员工',
            'type': '货物类型',
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
    class Meta:
        model = Staff
        fields = ['staff_id', 'name', 'phone', 'email', 'national_id', 'position', 'employed_date']

        widgets = {
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.ModelChoiceField(queryset=Position.objects.all(), attrs={'class': 'form-control'}),
            'employed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }

        labels = {
            'staff_id': '工号',
            'name': '姓名',
            'phone': '手机号',
            'email': '邮箱',
            'national_id': '身份证号',
            'position': '职位',
            'employed_date': '入职日期'
        }


class PermsForm(forms.ModelForm):
    class Meta:
        model = Perm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PermsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            field.widget.attrs['class'] = 'form-check-input'
            field.widget.attrs['type'] = 'checkbox'
            field.widget.attrs['role'] = 'switch'
            field.widget.attrs['id'] = 'flexSwitchCheckDefault'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']

        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}
