from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

# Create your views here.
from Compra.forms import CompraForm,NotaCompraForm
from Compra.models import Compra, DetCompra,NotaCreditoCompra,DetNotaCreditoCompra
from Producto.models import Producto
import json
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
#from xhtml2pdf import pisa


class CompraListview(ListView):
    model = Compra
    template_name = 'lista_compra_original.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Compra.objects.all():
                    i.id=str(i.id).zfill(6)
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetCompra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['boton'] = 'Compra'
        context['create_url'] = reverse_lazy('Agregar compra')
        context['list_url'] = reverse_lazy('Listado de compras')
        context['entity'] = 'Compra'

        return context


class CompraCreateView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'create_compra.html'
    success_url = reverse_lazy('Listado de compras')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['compr'])
                    compra = Compra()
                    compra.fecha_compra = vents['fecha_compra']
                    compra.fecha_vencimiento = vents['fecha_vencimiento']
                    compra.prov_datos_id = vents['prov_datos']
                    compra.pago = vents['pago']
                    compra.subtotal = float(vents['subtotal'])
                    compra.iva = float(vents['iva'])
                    compra.total = float(vents['total'])
                    compra.save()
                    for i in vents['products']:
                        det = DetCompra()
                        det.compra_id = compra.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio_costo'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': compra.id}
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
        context['title'] = 'Agregar Compra'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Compra'
        return context


class CompraUpdateView(UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'create_compra_edit.html'
    success_url = reverse_lazy('Listado de compras')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['compr'])
                    compra = Compra.objects.get(pk=self.get_object().id)
                    compra.fecha_compra = vents['fecha_compra']
                    compra.fecha_vencimiento = vents['fecha_vencimiento']
                    compra.prov_datos_id = vents['prov_datos']
                    compra.pago = vents['pago']
                    compra.subtotal = float(vents['subtotal'])
                    compra.iva = float(vents['iva'])
                    compra.total = float(vents['total'])
                    compra.save()
                    for i in vents['products']:
                        det = DetCompra()
                        det.compra_id = compra.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio_costo'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # det.prod.stock += det.cant
                        # det.prod.save()
                    data = {'id': compra.id}
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = Producto.objects.all()  # filter(stock__gt=0)
                if len(term):
                    products = products.filter(nombre__icontains=term)
                for i in products[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetCompra.objects.filter(compra_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Compra'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), default=str)
        context['entity'] = 'Compra'
        return context


class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'delete_venta.html'
    success_url = reverse_lazy('Listado de compras')

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
        context['title'] = 'Eliminación de una Compra'
        context['entity'] = 'Compra'
        context['list_url'] = self.success_url
        return context


class NotaCompraListview(ListView):
    model = NotaCreditoCompra
    template_name = 'lista_Nota_credito_compra_original.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                print('entra a searchdata')
                data = []
                for i in NotaCreditoCompra.objects.all():
                    #i.id =str(i.detcompra_datos.id).zfill(6)
                   # print(i.id)
                    #print(i.total)
                    data.append(i.toJSON())
                    #for j in DetNotaCreditoCompra.objects.all():
                #.filter(notacredito_id=request.POST['id']):
                        #print(j.notacredito_id)
                        #data.append(j.toJSON()) 
            elif action == 'search_details_prod':
                print('entra a search_details_prod')
                data = []
                for i in DetNotaCreditoCompra.objects.filter(notacredito_id=request.POST['id']):
                    print(i.totalnota)
                    data.append(i.toJSON())    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Nota Compras'
        context['boton'] = 'Nota Credito Compra'
        context['create_url'] = reverse_lazy('Agregar Nota Credito Compra')
        context['list_url'] = reverse_lazy('Listado de Nota Credito Compra')
        context['entity'] = 'Nota Credito Compra'

        return context


class NotaCreditoProveedorCreateView(CreateView):
    model = NotaCreditoCompra
    form_class = NotaCompraForm
    template_name = 'create_nota_compra.html'
    success_url = reverse_lazy('Listado de Nota Credito Compra')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                print('entra en add')
                with transaction.atomic():
                    vents = json.loads(request.POST['compr'])
                    #nota = NotaCreditoCompra.objects.all()
                    nota = NotaCreditoCompra()
                    nota.fecha_emision_nota = vents['fecha_emision_nota']
                    nota.total= vents['total']
                    nota.save()
                    for i in vents['products']:
                        #nota = NotaCreditoCompra()
                        detnota = DetNotaCreditoCompra()
                        detnota.notacredito_id = nota.id
                        detnota.detcompra_datos_id = i['id']
                        detnota.compra_id =i['id']
                        detnota.totalnota = i['subtotal']
                        detnota.cantnota = i['cant']                   
                        detnota.desc = i['desc']
                        detnota.save()
                    #data = {'id': nota.id}
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = DetCompra.objects.all()  # filter(stock__gt=0)
                if len(term):
                    products = DetCompra.filter(id=term)
                for i in products[0:10]:
                    item = i.toJSON()
                    item['value'] = i.id 
                    item['id'] = str(i.compra_id).zfill(6)
                    item['prov_datos']=i.compra.prov_datos.nombre
                    item['total'] = i.compra.total
                    #item['subtotal'] = i.compra.subtotal
                    # item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Compra'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Compra'
        return context

class NotaCreditoProveedorDeleteView(DeleteView):
    model = NotaCreditoCompra
    template_name = 'delete_nota_compra.html'
    success_url = reverse_lazy("Listado de Nota Credito Compra")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Nota Credito Compra'
        context['list_url'] = reverse_lazy("Listado de Nota Credito Compra")
        context['entity'] = 'Nota Credito Compra'
        return context


class SaleInvoicePdfView(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        compra = Compra.objects.get(pk=self.kwargs['pk']).id
        Detcompra = DetCompra.objects.all().filter(compra_id=compra)
        estado_fact = Compra.objects.get(pk=self.kwargs['pk']).es_procesado
        print(estado_fact)
        if estado_fact == 'N':
            for i in Detcompra:
               i.prod.stock = i.prod.stock + i.cant
               i.compra.es_procesado = 'S'
               i.prod.save()
               i.compra.save()
        try:
            template = get_template('invoice_compra.html')
            context = {
                'compra': Compra.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'AguaMarina', 'ruc': '9999999999999',
                         'address': 'Avda Fernando de la Mora esq Taruma'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Listado de compras'))
