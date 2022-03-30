from django.forms import *
from django.forms import ModelForm, TextInput
from django import forms
from Venta.models import *
from datetime import datetime


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Ingrese nombre del cliente',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    # 'class': 'form-control',
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    # 'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'pago': Select(attrs={
                'class': 'form-control select2',
                # 'style': 'width: 100%'
            }),
        }
