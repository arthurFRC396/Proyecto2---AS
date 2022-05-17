from django.forms import *
from django.forms import ModelForm, TextInput
from django import forms
from Caja.models import *
from datetime import datetime
from crum import get_current_request


class CajaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Caja
        fields = 'id','usuario','fecha_inicio', 'fecha_cierre', 'monto_inicial', 'monto_final', 'total_venta', 'status'
        widgets = {
            # 'fecha_inicio': forms.DateInput(
            #     # format='YYYY-MM-DD',
            #     attrs={
            #         'value': datetime.now().strftime('YYYY-MM-DD'),
            #         'autocomplete': 'off',
            #         'class': 'form-control datetimepicker-input',
            #         'id': 'fecha_inicio',
            #         'data-target': '#fecha_inicio',
            #         'data-toggle': 'datetimepicker'
            #     }),
            # 'fecha_cierre': forms.DateInput(
            #     # format='YYYY-MM-DD',
            #     attrs={
            #         'value': datetime.now().strftime('YYYY-MM-DD'),
            #         'autocomplete': 'off',
            #         'class': 'form-control datetimepicker-input',
            #         'id': 'fecha_cierre',
            #         'data-target': '#fecha_cierre',
            #         'data-toggle': 'datetimepicker'
            #     }),
            'monto_inicial': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del monto inicial',
                }),
            'monto_final': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del monto final',
                }),
            'total_venta': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero del monto final',
                }),
            'status': Select()
        }
        exclude = ['usuario','monto_final','fecha_cierre', 'total_venta']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                request = get_current_request()
                c=form.save(commit=False)
                c.usuario= request.user
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
