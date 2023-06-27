from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    credible = forms.BooleanField(
        required=False,
    )

    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address', 'credible')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'credible': forms.CheckboxInput(attrs={'class': 'form-control', 'value': 'checked'}),
        }
