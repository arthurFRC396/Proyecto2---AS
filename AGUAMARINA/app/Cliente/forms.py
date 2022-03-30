from django.forms import *
from django.forms import ModelForm, TextInput
from django import forms
from Cliente.models import *
from datetime import datetime


class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        # form.field.widget.attrs['class'] = 'form-control'
        # form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombres del cliente',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese apellidos del cliente',
                }
            ),
            'ci': TextInput(
                attrs={
                    'placeholder': 'Ingrese numero de cedula',
                }
            ),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese el RUC',
                }
            ),
            'nacimiento': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'nacimiento',
                    'data-target': '#nacimiento',
                    'data-toggle': 'datetimepicker'
                }),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion del cliente',
                }),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono del cliente',
                }),
            'genero': Select()
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
