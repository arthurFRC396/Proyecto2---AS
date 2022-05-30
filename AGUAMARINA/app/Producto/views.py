import datetime
from unicodedata import decimal

import app.settings
from Producto.models import *
from Producto.forms import TipoProductoForm, ProductoForm, OfertaForm, OfertaUpdateForm, ProductoUpdateForm,InventarioForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy,reverse
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.utils.timezone import now
from datetime import *
from django.db import connection,transaction
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.shortcuts import render

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
            # print('Producto', i.id)
            fechaActual = now().date() + timedelta(days=0)
            for j in ofer:
                # print('oferta', j.producto_cod)
                if str(i.id) == str(j.producto_cod):
                    producto_oferta = Producto.objects.get(id=i.id)
                    # print(producto_oferta.es_oferta)
                    if (fechaActual >= j.fecha_inicio_oferta) and (fechaActual <= j.fecha_fin_oferta):
                        if producto_oferta.es_oferta == 'N':
                            if producto_oferta.stock > 0:
                                if producto_oferta.chk_oferta == 0:
                                    ofer_temp = Oferta_temp.objects.all()
                                    producto_oferta.es_oferta = 'S'
                                    descuento = producto_oferta.precio_venta * (j.porcentaje_descuento / 100)
                                    producto_oferta.precio_venta -= descuento
                                    # print('Nuevo:')
                                    # print(producto_oferta.es_oferta)
                                    # print(producto_oferta.precio_venta)
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

                # else:
                #     print('son distintos')

    def PrecioAnterior():
        prod = Producto.objects.all()
        ofer = Oferta.objects.all()
        lista_temp = []
        cod_prod_temp = 0
        precio_oferta = 0
        for i in prod:
            # print('Producto', i.id)
            fechaActual = now().date() + timedelta(days=0)
            for j in ofer:
                # print('oferta', j.producto_cod)
                if str(i.id) == str(j.producto_cod):
                    producto_oferta = Producto.objects.get(id=i.id)
                    # print(producto_oferta.es_oferta)
                    if (fechaActual >= j.fecha_inicio_oferta) and (fechaActual <= j.fecha_fin_oferta):
                        if producto_oferta.es_oferta == 'N':
                            if producto_oferta.stock > 0:
                                if producto_oferta.chk_oferta == 0:
                                    ofer_temp = Oferta_temp.objects.all()
                                    producto_oferta.es_oferta = 'S'
                                    descuento = producto_oferta.precio_venta * (j.porcentaje_descuento / 100)
                                    producto_oferta.precio_venta -= descuento
                                    # print('Nuevo:')
                                    # print(producto_oferta.es_oferta)
                                    # print(producto_oferta.precio_venta)
                                    producto_oferta.save()
                                    if ofer_temp.exists():
                                        for k in ofer_temp:
                                            if k.oferta_cod == producto_oferta.id:
                                                k.porcentaje_descuento = j.porcentaje_descuento
                                                # print('temp_cod: ', ofer_temp.oferta_cod)
                                                # print('temp_porcent: ', ofer_temp.porcentaje_descuento)
                                                k.save()
                                            else:
                                                ofer_temp.create(oferta_cod=producto_oferta.id,
                                                                 porcentaje_descuento=j.porcentaje_descuento)
                                    else:
                                        ofer_temp.create(oferta_cod=producto_oferta.id, porcentaje_descuento=j.porcentaje_descuento)
                # else:
                #     print('son distintos')


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

############## vista Inventario #################################
def home(request):
    if request.method == "POST":
        file2 = request.FILES["file"]
        document = FilesUploads.objects.create(file=file2)
        document.save()
        return HttpResponseRedirect(reverse('Listado De Ajustes de Inventario'))
    return render(request,'adjunto.html')

class InventarioListview(ListView):
    model = Inventario
    template_name = 'lista_inventario.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Inventario.objects.all():
                    i.id=str(i.id).zfill(6)
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetInventario.objects.filter(inventario_id=request.POST['id']):
                    i.prod_id=str(i.prod_id).zfill(6)
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado De Ajustes de Inventario'
        context['boton'] = 'Ajuste'
        context['create_url'] = reverse_lazy('Ajustar Inventario')
        context['list_url'] = reverse_lazy('Listado De Ajustes de Inventario')
        context['entity'] = 'Inventario'

        return context



class InventarioCreateView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'create_inventario.html'
    success_url = reverse_lazy('Listado De Ajustes de Inventario')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['invent'])
                    inventario = Inventario()
                    inventario.fecha_registro = vents['fecha_registro']
                    inventario.save() 
                    for i in vents['products']:
                        det = DetInventario()
                        det.inventario_id = inventario.id
                        det.prod_id = i['id']
                        det.cantprod = int(i['cant'])
                        det.motivo = i['motivo']
                        det.save()
                    data = {'id': inventario.id}
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = Producto.objects.all()  # filter(stock__gt=0)
                if len(term):
                    products = products.filter(nombre__icontains=term)
                for i in products[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    # item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajustar Inventario'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Inventario'
        return context


class InventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'create_inventario_edit.html'
    success_url = reverse_lazy('Listado De Ajustes de Inventario')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['invent'])
                    inventario = Inventario.objects.get(pk=self.get_object().id)
                    inventario.fecha_registro = vents['fecha_registro']
                    inventario.save()
                    inventario.detinventario_set.all().delete()
                    for i in vents['products']:
                        det = DetInventario()
                        det.inventario_id = inventario.id
                        det.prod_id = i['id']
                        det.cantprod = int(i['cant'])
                        det.motivo = i['motivo']
                        det.save()
                    data = {'id': inventario.id}
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = Producto.objects.all()  # filter(stock__gt=0)
                if len(term):
                    products = products.filter(nombre__icontains=term)
                for i in products[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    # item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetInventario.objects.filter(inventario_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cantprod
                #item['motivo'] = i.motivo
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Ajuste'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), default=str)
        context['entity'] = 'Ajuste'
        return context

class InventarioDeleteView(DeleteView):
    model = Inventario
    template_name = 'delete_inventario.html'
    success_url = reverse_lazy('Listado De Ajustes de Inventario')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Ajuste'
        context['entity'] = 'Inventario'
        context['list_url'] = self.success_url
        return context

class InventarioAjusteView(View):

    def get(self, request, *args, **kwargs):
        inventario = Inventario.objects.get(pk=self.kwargs['pk']).id
        detajuste = DetInventario.objects.all().filter(inventario_id=inventario)
        estado_ajuste = Inventario.objects.get(pk=self.kwargs['pk']).es_procesado
        print(estado_ajuste)
        if estado_ajuste == 'N':
            for i in detajuste:
                print(i.cantprod)
                i.prod.stock = i.prod.stock - i.cantprod
                i.inventario.es_procesado = 'S'
                i.prod.save()
                i.inventario.save()
            return HttpResponseRedirect(reverse('Listado De Ajustes de Inventario'))


