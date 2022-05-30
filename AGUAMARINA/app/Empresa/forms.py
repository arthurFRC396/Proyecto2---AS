from django.forms import *
from django.forms import ModelForm, TextInput
from django import forms
from Empresa.models import *
from datetime import datetime


class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de la empresa',
                }
            ),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese el RUC de la empresa',
                }
            ),
            'timbrado': TextInput(
                attrs={
                    'placeholder': 'Ingrese el timbrado vigente',
                }
            ),
            'establecimiento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del establecimiento',
                    'value': '',
                }
            ),
            'punto_expedicion': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del punto de expedicion',
                }
            ),
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
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion de la empresa',
                }),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono de la empresa',
                }),
            'correo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico de la empresa',
                })
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

class EmpresaupdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = ('nombre', 'ruc','timbrado', 'establecimiento','punto_expedicion', 'fecha_vencimiento','direccion', 'telefono','correo')
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de la empresa',
                }
            ),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese el RUC de la empresa',
                }
            ),
            'timbrado': TextInput(
                attrs={
                    'placeholder': 'Ingrese el timbrado vigente',
                }
            ),
            'establecimiento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del establecimiento',
                    'value': '',
                }
            ),
            'punto_expedicion': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del punto de expedicion',
                }
            ),
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
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion de la empresa',
                }),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono de la empresa',
                }),
            'correo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico de la empresa',
                })
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
