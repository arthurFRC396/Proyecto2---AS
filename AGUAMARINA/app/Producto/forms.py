from django.forms import ModelForm, TextInput
from django import forms
from Producto.models import *
from datetime import datetime


class TipoProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = TipoProducto
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del tipo de producto',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese descripcion del tipo de producto',
                }
            ),
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


class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = 'nombre', 'marca', 'tipo_producto', 'proveedor', 'precio_costo', 'precio_venta', 'stock', 'descripcion'
        widgets = {

            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del producto',
                }
            ),
            'marca': TextInput(
                attrs={
                    'placeholder': 'Ingrese la marca del producto',
                }
            ),
            'tipo_producto': forms.Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'precio_costo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el precio de costo del producto',
                }
            ),
            'precio_venta': TextInput(
                attrs={
                    'placeholder': 'Ingrese el precio de venta del producto',
                }
            ),
            'stock': TextInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad adquirida del producto',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese descripcion del producto',
                }
            ),
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


class ProductoUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = ('nombre', 'marca', 'tipo_producto', 'proveedor', 'descripcion')
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del producto',
                }
            ),
            'marca': TextInput(
                attrs={
                    'placeholder': 'Ingrese la marca del producto',
                }
            ),
            'tipo_producto': forms.Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'proveedor': forms.Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'precio_costo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el precio de costo del producto',
                }
            ),
            'precio_venta': TextInput(
                attrs={
                    'placeholder': 'Ingrese el precio de venta del producto',
                }
            ),
            'stock': TextInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad adquirida del producto',
                }
            ),
            'es_oferta': TextInput(
                attrs={
                    'placeholder': 'El producto se encuentra en oferta (S/N)',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese descripcion del producto',
                }
            ),
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


class OfertaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['porcentaje_descuento'].widget.attrs['autofocus'] = True

    class Meta:
        model = Oferta
        fields = '__all__'
        widgets = {
            'producto_cod': forms.Select(attrs={
                'class': 'form-control select2',
                'placeholder': 'Ingrese codigo o nombre de producto',
                # 'style': 'width: 100%'
            }),
            'porcentaje_descuento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el porcentaje de descuento del producto',
                }
            ),
            'fecha_inicio_oferta': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_inicio_oferta',
                    'data-target': '#fecha_inicio_oferta',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'fecha_fin_oferta': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_fin_oferta',
                    'data-target': '#fecha_fin_oferta',
                    'data-toggle': 'datetimepicker'
                }
            ),
            # 'ingresado': forms.DateInput(
            #     format='DD/MM/YYYY HH:mm:ss',
            #     attrs={
            #         'value': datetime.now().strftime('DD/MM/YYYY HH:mm:ss'),
            #         'autocomplete': 'off',
            #         'class': 'form-control datetimepicker-input',
            #         'id': 'ingresado',
            #         'data-target': '#ingresado',
            #         'data-toggle': 'datetimepicker'
            #     }
            # ),
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


class OfertaUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['producto_lote'].widget.attrs['autofocus'] = True

    class Meta:
        model = Oferta
        fields = ('fecha_inicio_oferta', 'fecha_fin_oferta','porcentaje_descuento')
        widgets = {
            'fecha_inicio_oferta': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_inicio_oferta',
                    'data-target': '#fecha_inicio_oferta',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'porcentaje_descuento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el porcentaje de descuento del producto',
                }
            ),
            'fecha_fin_oferta': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={
                    'value': datetime.now().strftime('YYYY-MM-DD'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_fin_oferta',
                    'data-target': '#fecha_fin_oferta',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'ingresado': forms.DateInput(
                format='DD/MM/YYYY HH:mm:ss',
                attrs={
                    'value': datetime.now().strftime('DD/MM/YYYY HH:mm:ss'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'ingresado',
                    'data-target': '#ingresado',
                    'data-toggle': 'datetimepicker'
                }
            ),
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
