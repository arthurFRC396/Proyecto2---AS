import datetime
import json

from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from Cliente.forms import ClienteForm
from Cliente.models import Cliente
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic import TemplateView

# Create your views here.
from Producto.models import Producto
from Venta.forms import SaleForm, NotaVentaForm
from Venta.models import Sale, DetSale, NotaCreditoVenta,DetNotaCreditoVenta
from user.models import User
from Empresa.models import Empresa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime,timedelta,date



class SaleListView(ListView):
    model = Sale
    template_name = 'list_venta.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())                     
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('Agregar Venta')
        context['list_url'] = reverse_lazy('Listado de Venta')
        context['entity'] = 'Facturas'
        context['boton'] = 'Venta'
        return context


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'create_venta.html'
    success_url = reverse_lazy("Listado de Venta")

    # url_redirect = success_url

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = Producto.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(nombre__icontains=term)
                for i in products[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Producto.objects.filter(nombre__icontains=term, stock__gt=0)
                for i in products[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.nombre
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.pago = vents['pago']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.usuario_id = request.user.id
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio_venta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # det.prod.stock -= det.cant
                        # det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Cliente.objects.filter(
                    Q(nombre__icontains=term) | Q(apellido__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClienteForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Agregar Venta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['entity'] = 'Venta'
        return context


class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'create_venta_Edit.html'
    success_url = reverse_lazy("Listado de Venta")

    # url_redirect = success_url

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = Producto.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(nombre__icontains=term)
                for i in products[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Producto.objects.filter(nombre__icontains=term, stock__gt=0)
                for i in products[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.nombre
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale.objects.get(pk=self.get_object().id)
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.pago = vents['pago']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    # se elimina el detalle para evitar duplicidad
                    sale.detsale_set.all().delete()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio_venta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        # det.prod.stock -= det.cant
                        # det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Cliente.objects.filter(
                    Q(nombre__icontains=term) | Q(apellido__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClienteForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)

        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Editar Venta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), default=str)
        context['entity'] = 'Venta'
        return context



class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'delete_venta.html'
    success_url = reverse_lazy('Listado de Venta')

    # url_redirect = success_url

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
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class NotaVentaListview(ListView):
    model = NotaCreditoVenta
    template_name = 'lista_Nota_credito_venta_original.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in NotaCreditoVenta.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetNotaCreditoVenta.objects.filter(notacredito_id=request.POST['id']):
                    data.append(i.toJSON())    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Nota Ventas'
        context['boton'] = 'Nota Credito Venta'
        context['create_url'] = reverse_lazy('Agregar Nota Credito Venta')
        context['list_url'] = reverse_lazy('Listado de Nota Credito Venta')
        context['entity'] = 'Nota Credito Venta'

        return context


class NotaCreditoVentaCreateView(CreateView):
    model = NotaCreditoVenta
    form_class = NotaVentaForm
    template_name = 'create_nota_venta.html'
    success_url = reverse_lazy('Listado de Nota Credito Venta')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vent'])
                    nota = NotaCreditoVenta()
                    nota.fecha_emision_nota = vents['fecha_emision_nota']
                    nota.total= vents['total']
                    nota.save()
                    for i in vents['products']:
                        detnota = DetNotaCreditoVenta()
                        detnota.notacredito_id = nota.id
                        detnota.detventa_datos_id = i['id']
                        detnota.sale_id =i['id']
                        detnota.totalnota = i['subtotal']
                        detnota.cantnota = i['cant']                   
                        detnota.desc = i['desc']
                        detnota.save()
                    #data = {'id': nota.id}
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                products = DetSale.objects.all()  # filter(stock__gt=0)
                if len(term):
                    products = DetSale.filter(id=term)
                    
                for i in products[0:10]:
                    if (i.sale.es_procesado) == 'S':
                        item = i.toJSON()
                        item['value'] = i.id 
                        item['id'] = str(i.sale_id).zfill(6)
                        item['cli']=i.sale.cli.nombre
                        item['total'] = i.sale.total
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
        context['title'] = 'Agregar Nota'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['entity'] = 'Nota'
        return context



class SaleInvoicePdfView(View):
    model = Sale
    form_class = SaleForm


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
        Venta = Sale.objects.get(pk=self.kwargs['pk']).id
        DetVenta = DetSale.objects.all().filter(sale_id=Venta)
        estado_fact = Sale.objects.get(pk=self.kwargs['pk']).es_procesado
        empresa_datos = Empresa.objects.all()
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        nombre_empresa=''
        ruc_empresa=''
        direccion_empresa=''
        timbrado_empresa =''

        for e in empresa_datos:
            if e.estado =='A':
                empresa_venc = e.fecha_vencimiento
                if str(fecha_hoy) <= str(empresa_venc):
                    nuevo_timb = e.timbrado+1
                    nombre_empresa=e.nombre
                    ruc_empresa=e.ruc
                    direccion_empresa=e.direccion
                    e.timbrado = nuevo_timb
                    timbrado_empresa = e.establecimiento +' - '+ e.punto_expedicion +' - '+ str(nuevo_timb).zfill(6)
                    e.estado = 'A'
                    e.save()
                else:
                    nombre_empresa=e.nombre
                    ruc_empresa=e.ruc
                    direccion_empresa=e.direccion
                    timbrado_empresa = e.establecimiento +' - '+ e.punto_expedicion +' - '+ str(e.timbrado).zfill(6)+' TIMBRADO VENCIDO'
                    e.estado = 'I'
                    e.save()
            else:
                    nombre_empresa=e.nombre
                    ruc_empresa=e.ruc
                    direccion_empresa=e.direccion
                    timbrado_empresa = e.establecimiento +' - '+ e.punto_expedicion +' - '+ str(e.timbrado).zfill(6)+' TIMBRADO VENCIDO'

        if estado_fact == 'N':
            for i in DetVenta:
                i.prod.stock = i.prod.stock - i.cant
                i.sale.es_procesado = 'S'
                i.prod.save()
                i.sale.save()

        try:

            template = get_template('invoice.html')

            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': nombre_empresa, 'ruc': ruc_empresa,
                         'address': direccion_empresa,
                         'timbrado':timbrado_empresa},
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


class dashventaview(ListView):
    model = Sale
    template_name = 'dashboard_venta.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'totalventa':
                datos = []
                a=0
                enero=0;febrero=0;marzo=0;abril=0;mayo=0;junio=0;julio=0;agosto=0;septiembre=0;octubre=0;noviembre=0;diciembre=0

                for i in Sale.objects.all():
                    if i.date_joined.year == datetime.today().year:
                        if i.date_joined.month == 1:
                            enero+=i.total
                        elif i.date_joined.month== 2:
                            febrero+=i.total
                        elif i.date_joined.month== 3:
                            marzo+=i.total
                        elif i.date_joined.month== 4:
                            abril+=i.total
                        elif i.date_joined.month== 5:
                            mayo+=i.total
                        elif i.date_joined.month== 6:
                            junio+=i.total
                        elif i.date_joined.month== 7:
                            julio+=i.total
                        elif i.date_joined.month== 8:
                            agosto+=i.total
                        elif i.date_joined.month== 9:
                            septiembre+=i.total
                        elif i.date_joined.month== 10:
                            octubre+=i.total
                        elif i.date_joined.month== 11:
                            noviembre+=i.total
                        elif i.date_joined.month== 12:
                            diciembre+=i.total
                datos.append(enero);datos.append(febrero);datos.append(marzo);datos.append(abril);datos.append(mayo);datos.append(junio)
                datos.append(julio);datos.append(agosto);datos.append(septiembre);datos.append(octubre);datos.append(noviembre);datos.append(diciembre)
            elif action == 'totalsemana':
                print('totalsemana')
                datos = []
                a=0
                lunes=0;martes=0;miercoles=0;jueves=0;viernes=0;sabado=0;domingo=0
                cant_lunes=0;cant_martes=0;cant_miercoles=0;cant_jueves=0;cant_viernes=0;cant_sabado=0;cant_domingo=0
                today_date = date.today()
                print('antes del if')
                if datetime.today().isoweekday() == 1:
                    td_dom = timedelta(6)
                    lunes_semana = today_date
                    domingo_semana = today_date + td_dom
                if datetime.today().isoweekday()== 2:
                    td_lun = timedelta(1)
                    td_dom = timedelta(5)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                if datetime.today().isoweekday()== 3:
                    td_lun = timedelta(2)
                    td_dom = timedelta(4)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                if datetime.today().isoweekday()== 4:
                    td_lun = timedelta(3)
                    td_dom = timedelta(3)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                if datetime.today().isoweekday()== 5:
                    td_lun = timedelta(4)
                    td_dom = timedelta(2)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                if datetime.today().isoweekday()== 6:
                    td_lun = timedelta(5)
                    td_dom = timedelta(1)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                if datetime.today().isoweekday()== 7:
                    td_lun = timedelta(6)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date
                    
                # print('lunes'+str(lunes_semana))
                # print('domingo'+str(domingo_semana))
                # print('antes del for')
                for i in Sale.objects.all(): 
                    if i.date_joined.year == datetime.today().year:
                        if i.date_joined.month == datetime.today().month:
                            if (str(i.date_joined.strftime('%Y-%m-%d')) >= str(lunes_semana)) and (str(i.date_joined.strftime('%Y-%m-%d')) <= str(domingo_semana)):
                                print('semana')
                                if i.date_joined.isoweekday() == 1:
                                    lunes+=i.total
                                elif i.date_joined.isoweekday()== 2:
                                    martes+=i.total
                                elif i.date_joined.isoweekday()== 3:
                                    miercoles+=i.total
                                elif i.date_joined.isoweekday()== 4:
                                    jueves+=i.total
                                elif i.date_joined.isoweekday()== 5:
                                    viernes+=i.total
                                elif i.date_joined.isoweekday()== 6:
                                    sabado+=i.total
                                elif i.date_joined.isoweekday()== 7:
                                    domingo+=i.total
                datos.append(lunes);datos.append(martes);datos.append(miercoles);datos.append(jueves);datos.append(viernes);datos.append(sabado);datos.append(domingo)
            elif action == 'prodmasvendido':
                datos = []
                tipos = []
                cantidad = []
                can_prod=0
                today_date = date.today()

                if datetime.today().isoweekday() == 1:
                    td_dom = timedelta(6)
                    lunes_semana = today_date
                    domingo_semana = today_date + td_dom
                elif datetime.today().isoweekday()== 2:
                    td_lun = timedelta(1)
                    td_dom = timedelta(5)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                elif datetime.today().isoweekday()== 3:
                    td_lun = timedelta(2)
                    td_dom = timedelta(4)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom                         
                elif datetime.today().isoweekday()== 4:
                    td_lun = timedelta(3)
                    td_dom = timedelta(3)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                elif datetime.today().isoweekday()== 5:
                    td_lun = timedelta(4)
                    td_dom = timedelta(2)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                elif datetime.today().isoweekday()== 6:
                    td_lun = timedelta(5)
                    td_dom = timedelta(1)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date + td_dom
                elif datetime.today().isoweekday()== 7:
                    td_lun = timedelta(6)
                    lunes_semana = today_date - td_lun
                    domingo_semana = today_date

                #se almacena los tipos de productos
                for t in Producto.objects.all():
                    tipos.append(t.tipo_producto.nombre)
                for e in tipos:
                    for d in DetSale.objects.all():
                        if d.sale.date_joined.year == datetime.today().year:
                            if d.sale.date_joined.month == datetime.today().month:
                                if (str(d.sale.date_joined.strftime('%Y-%m-%d')) >= str(lunes_semana)) and (str(d.sale.date_joined.strftime('%Y-%m-%d')) <= str(domingo_semana)):
                                    if str(d.prod.tipo_producto.nombre) == str(e):
                                        can_prod+=d.cant
                    cantidad.append(can_prod)
                    can_prod=0
                largo = range(len(cantidad))
                print(largo)
                for a in largo:
                    if a % 2 == 0:
                        datos.append(tipos[a])
                        datos.append(cantidad[a])
                    else:
                        datos.append(tipos[a])
                        datos.append(cantidad[a])

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(datos, safe=False)


