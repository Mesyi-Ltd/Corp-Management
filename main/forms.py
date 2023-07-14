from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    credible = forms.BooleanField(
        required=False,
    )

    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),

        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'order_id': forms.TextInput(attrs={'class': 'form-control', }),
            'handed': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'})
        }

        labels = {
            'order_id': '订单号'
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

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
