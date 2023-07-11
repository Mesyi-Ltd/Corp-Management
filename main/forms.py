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

