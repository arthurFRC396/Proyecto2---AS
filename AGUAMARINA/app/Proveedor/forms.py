from django.forms import *
from django.forms import ModelForm, TextInput
from django import forms
from Proveedor.models import *
from datetime import datetime


class ProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proveedor',
                }
            ),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese el RUC',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion del proveedor',
                }),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono del proveedor',
                }),
            'correo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el E-Mail del proveedor',
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
