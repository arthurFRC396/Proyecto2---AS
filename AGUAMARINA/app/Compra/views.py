from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

# Create your views here.
from Compra.forms import CompraForm
from Compra.models import Compra, DetCompra
from Producto.models import Producto
import json
import os
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
#from xhtml2pdf import pisa

class CompraListview(ListView):
    model = Compra
    template_name = 'lista_compra.html'

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
                        print(det.prod.stock)
                        det.save()
                        det.prod.stock += det.cant
                        det.prod.save()
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
        try:
            template = get_template('invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('Listado de Venta'))
