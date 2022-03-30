import datetime
from unicodedata import decimal

import app.settings
from Producto.models import *
from Producto.forms import TipoProductoForm, ProductoForm, OfertaForm, OfertaUpdateForm, ProductoUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.timezone import now
from datetime import *
from django.db import connection


class TipoProductoListview(ListView):
    model = TipoProducto
    template_name = 'lista_tipo_producto.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TipoProducto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Producto'
        context['boton'] = 'Tipo de Producto'
        context['create_url'] = reverse_lazy("Agregar Tipo De Producto")
        context['list_url'] = reverse_lazy("Listado Tipos De Producto")
        context['entity'] = 'Tipo de Producto'
        return context


class TipoProductoCreateView(CreateView):
    model = TipoProducto
    form_class = TipoProductoForm
    template_name = 'create_tipo_producto.html'
    success_url = reverse_lazy("Listado Tipos De Producto")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Agregar Tipo Producto'
        context['list_url'] = reverse_lazy("Listado Tipos De Producto")
        context['action'] = 'add'
        context['entity'] = 'Tipo de Producto'
        return context


class TipoProductoUpdateView(UpdateView):
    model = TipoProducto
    form_class = TipoProductoForm
    template_name = 'create_tipo_producto.html'
    success_url = reverse_lazy("Listado Tipos De Producto")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Editar Tipo Producto'
        context['list_url'] = reverse_lazy("Listado Tipos De Producto")
        context['action'] = 'edit'
        context['entity'] = 'Tipo de Producto'
        return context


class TipoProductoDeleteView(DeleteView):
    model = TipoProducto
    template_name = 'delete_tipo_producto.html'
    success_url = reverse_lazy("Listado Tipos De Producto")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Tipo De Producto'
        context['list_url'] = reverse_lazy("Listado Tipos De Producto")
        context['entity'] = 'Tipo de Producto'
        return context


############## vista producto #################################


class ProductoListview(ListView):
    model = Producto
    template_name = 'lista_producto.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Producto'
        context['boton'] = 'Producto'
        context['create_url'] = reverse_lazy("Agregar Producto")
        context['list_url'] = reverse_lazy("Listado De Producto")
        context['entity'] = 'Producto'
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'create_producto.html'
    success_url = reverse_lazy("Listado De Producto")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Agregar Producto'
        context['list_url'] = reverse_lazy("Listado De Producto")
        context['action'] = 'add'
        context['entity'] = 'Producto'
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoUpdateForm
    template_name = 'create_producto.html'
    success_url = reverse_lazy("Listado De Producto")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto'
        context['list_url'] = reverse_lazy("Listado De Producto")
        context['action'] = 'edit'
        context['entity'] = 'Producto'
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'delete_producto.html'
    success_url = reverse_lazy("Listado De Producto")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['list_url'] = reverse_lazy("Listado De Producto")
        context['entity'] = 'Producto'
        return context


############## vista oferta #################################

class OfertaListview(ListView):
    model = Oferta
    template_name = 'list_oferta.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        OfertaListview.CalcularOferta()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Oferta.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ofertas'
        context['boton'] = 'Oferta'
        context['create_url'] = reverse_lazy("Agregar Oferta")
        context['list_url'] = reverse_lazy("Listado De Oferta")
        context['entity'] = 'Oferta'
        return context

    def CalcularOferta():
        prod = Producto.objects.all()
        ofer = Oferta.objects.all()
        lista_temp = []
        cod_prod_temp = 0
        precio_oferta = 0
        for i in prod:
            print('Producto', i.id)
            fechaActual = now().date() + timedelta(days=0)
            for j in ofer:
                print('oferta', j.producto_cod)
                if str(i.id) == str(j.producto_cod):
                    producto_oferta = Producto.objects.get(id=i.id)
                    print(producto_oferta.es_oferta)
                    if (fechaActual >= j.fecha_inicio_oferta) and (fechaActual <= j.fecha_fin_oferta):
                        if producto_oferta.es_oferta == 'N':
                            if producto_oferta.stock > 0:
                                if producto_oferta.chk_oferta == 0:
                                    ofer_temp = Oferta_temp.objects.all()
                                    producto_oferta.es_oferta = 'S'
                                    descuento = producto_oferta.precio_venta * (j.porcentaje_descuento / 100)
                                    producto_oferta.precio_venta -= descuento
                                    print('Nuevo:')
                                    print(producto_oferta.es_oferta)
                                    print(producto_oferta.precio_venta)
                                    producto_oferta.save()
                                    if ofer_temp.exists():
                                        for k in ofer_temp:
                                            if k.oferta_cod == producto_oferta.id:
                                                k.porcentaje_descuento = j.porcentaje_descuento
                                                k.save()
                                            else:
                                                ofer_temp.create(oferta_cod=producto_oferta.id,
                                                                 porcentaje_descuento=j.porcentaje_descuento)
                                    else:
                                        ofer_temp.create(oferta_cod=producto_oferta.id, porcentaje_descuento=j.porcentaje_descuento)
                    else:
                        if producto_oferta.es_oferta == 'S':
                            # if producto_oferta.stock > 0:
                            #     if producto_oferta.chk_oferta == 0:
                                    ofer_temp = Oferta_temp.objects.all()
                                    if ofer_temp.exists():
                                        for k in ofer_temp:
                                            if k.oferta_cod == producto_oferta.id:
                                                producto_oferta.es_oferta = 'N'
                                                producto_oferta.precio_venta = producto_oferta.precio_venta /(1-(k.porcentaje_descuento / 100))
                                                producto_oferta.save()
                                    #         else:
                                    #             ofer_temp.create(oferta_cod=producto_oferta.id,
                                    #                              porcentaje_descuento=j.porcentaje_descuento)
                                    # else:
                                    #     ofer_temp.create(oferta_cod=producto_oferta.id, porcentaje_descuento=j.porcentaje_descuento)

                else:
                    print('son distintos')

    def PrecioAnterior():
        prod = Producto.objects.all()
        ofer = Oferta.objects.all()
        lista_temp = []
        cod_prod_temp = 0
        precio_oferta = 0
        for i in prod:
            print('Producto', i.id)
            fechaActual = now().date() + timedelta(days=0)
            for j in ofer:
                print('oferta', j.producto_cod)
                if str(i.id) == str(j.producto_cod):
                    producto_oferta = Producto.objects.get(id=i.id)
                    print(producto_oferta.es_oferta)
                    if (fechaActual >= j.fecha_inicio_oferta) and (fechaActual <= j.fecha_fin_oferta):
                        if producto_oferta.es_oferta == 'N':
                            if producto_oferta.stock > 0:
                                if producto_oferta.chk_oferta == 0:
                                    ofer_temp = Oferta_temp.objects.all()
                                    producto_oferta.es_oferta = 'S'
                                    descuento = producto_oferta.precio_venta * (j.porcentaje_descuento / 100)
                                    producto_oferta.precio_venta -= descuento
                                    print('Nuevo:')
                                    print(producto_oferta.es_oferta)
                                    print(producto_oferta.precio_venta)
                                    producto_oferta.save()
                                    if ofer_temp.exists():
                                        for k in ofer_temp:
                                            if k.oferta_cod == producto_oferta.id:
                                                k.porcentaje_descuento = j.porcentaje_descuento
                                                print('temp_cod: ', ofer_temp.oferta_cod)
                                                print('temp_porcent: ', ofer_temp.porcentaje_descuento)
                                                k.save()
                                            else:
                                                ofer_temp.create(oferta_cod=producto_oferta.id,
                                                                 porcentaje_descuento=j.porcentaje_descuento)
                                    else:
                                        ofer_temp.create(oferta_cod=producto_oferta.id, porcentaje_descuento=j.porcentaje_descuento)
                else:
                    print('son distintos')
class OfertaCreateView(CreateView):
    model = Oferta
    form_class = OfertaForm
    template_name = 'create_oferta.html'
    success_url = reverse_lazy("Listado De Oferta")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Agregar Oferta'
        context['list_url'] = reverse_lazy("Listado De Oferta")
        context['action'] = 'add'
        context['entity'] = 'Oferta'
        return context


class OfertaUpdateView(UpdateView):
    model = Oferta
    form_class = OfertaUpdateForm
    template_name = 'create_oferta.html'
    success_url = reverse_lazy("Listado De Oferta")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Editar Oferta'
        context['list_url'] = reverse_lazy("Listado De Oferta")
        context['action'] = 'edit'
        context['entity'] = 'Oferta'
        return context


class OfertaDeleteView(DeleteView):
    model = Oferta
    template_name = 'delete_oferta.html'
    success_url = reverse_lazy("Listado De Oferta")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         self.object.delete()
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Oferta'
        context['list_url'] = reverse_lazy("Listado De Oferta")
        context['entity'] = 'Oferta'
        return context
