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



class NotaVentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = NotaCreditoVenta
        fields = '__all__'
        widgets = {
            'fecha_emision_nota': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'on',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_emision_nota',
                    'data-target': '#fecha_emision_nota',
                    'data-toggle': 'datetimepicker'
                }),
            'detventa_datos': Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Ingrese el numero de factura',
                # 'style': 'width: 100%'
            }),
            'desc_nota' : Textarea(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese el motivo de la nota',
                    'autocomplete' : 'off',
                    'id': 'desc_nota',
                    'rows' : 3,
                    'cols' : 3
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data