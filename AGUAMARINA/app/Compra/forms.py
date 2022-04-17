from datetime import datetime

from django.forms import ModelForm
from django.forms import *
from Compra.models import *
from django.forms import ModelForm, TextInput
from django.forms import *
from django.forms import ModelForm, TextInput
from django import forms


class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'fecha_compra': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_compra',
                    'data-target': '#fecha_compra',
                    'data-toggle': 'datetimepicker'
                }),
            'fecha_vencimiento': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_vencimiento',
                    'data-target': '#fecha_vencimiento',
                    'data-toggle': 'datetimepicker'
                }),
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
            'prov_datos': Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Ingrese nombre del Proveedor',
                # 'style': 'width: 100%'
            }),
            'cant_cuota': Select(attrs={
                'class': 'form-control select2',
                #'placeholder': 'Ingrese nombre del Proveedor',
                # 'style': 'width: 100%'
            }),
            'stock_actual': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'precio_unitario': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'pago': Select(attrs={
                'class': 'form-control select2',
                # 'style': 'width: 100%'
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),    
            'compra_id': Select(attrs={
                'class': 'form-control select2',
                'readonly': True
                #str(Compra.id).zfill(6),
            }),
            'desc' : Textarea(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese el motivo de la nota',
                    'autocomplete' : 'off',
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


class NotaCompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = NotaCreditoCompra
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
            'detcompra_datos': Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Ingrese el numero de factura',
                # 'style': 'width: 100%'
            }),
            'desc_nota' : Textarea(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese el motivo de la nota',
                    'autocomplete' : 'off',
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
