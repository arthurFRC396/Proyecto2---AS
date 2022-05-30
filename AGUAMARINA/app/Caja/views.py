
from datetime import *
from Caja.forms import CajaForm
from Caja.models import Caja
from Venta.models import Sale
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from user.models import User
from crum import get_current_request

class CajaListview(ListView):
    model = Caja
    template_name = 'lista_caja.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Caja.objects.all():
                    data.append(i.toJSON())
            elif action == 'bandera':
                data = []
                b=0
                for a in Caja.objects.all():
                    if str(a.status) == '1':
                        b+=1
                print(b)
                data.append(b)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de cajas'
        context['boton'] = 'Caja'
        context['create_url'] = reverse_lazy("Caja:agregar_cajas")
        context['list_url'] = reverse_lazy("Caja:listar_cajas")
        context['entity'] = 'Caja'
        return context


class CajaCreateView(CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'create_caja.html'
    success_url = reverse_lazy("dashboard")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                for j in User.objects.all():
                    if request.user.id == j.id:
                        print("entro al if") 
                        j.status= '1'
                        j.save()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Agregar caja'
        context['list_url'] = reverse_lazy("dashboard")
        context['action'] = 'add'
        context['entity'] = 'Caja'
        return context


class CajaUpdateView(UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'create_caja.html'
    success_url = reverse_lazy("Caja:listar_cajas")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                #para obtener el id de la caja actual con el request
                # request_actual = get_current_request()
                # request_actual = str(request_actual)
                # barra = '0'
                # ban=0
                # j=0
                # id_caja_actual= ''
                # for i in request_actual:
                #     if barra == '/':
                #         ban=1
                #     if j >= 33 and ban == 0:
                #         id_caja_actual = id_caja_actual + request_actual[j:j+1]
                #         barra = request_actual[j+1:j+2]
                #     j=j+1
                
                # print(id_caja_actual)
                
                # for j in Caja.objects.all():
                #     if j.id == int(id_caja_actual):
                #         print("entro al if")
                #         j.monto_final = j.monto_final - j.monto_inicial
                #         j.save()
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Editar caja'
        context['list_url'] = reverse_lazy("Caja:listar_cajas")
        context['action'] = 'edit'
        context['entity'] = 'Caja'
        return context


class CajaDeleteView(DeleteView):
    model = Caja
    template_name = 'delete_caja.html'
    success_url = reverse_lazy("Caja:listar_cajas")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    #
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if self.object.status == '1':
                for j in User.objects.all(): 
                    #si la caja a borrar esta abierta
                    # entonces que cambie el status a 2 
                    # si el usuario de caja a borrar es el mismo de la tabla user
                    if self.object.usuario_id == j.id:
                        j.status='2'
                        j.save()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Caja'
        context['list_url'] = reverse_lazy("Caja:listar_cajas")
        context['entity'] = 'Caja'
        return context

class CajaCerrarView(UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'create_caja.html'
    success_url = reverse_lazy("Caja:agregar_cajas")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        global monto_finals
        monto_finals = 0
        global total_ventas
        total_ventas = 0
        try:
            action = request.POST['action']
            if action == 'edit': 
                if self.object.status == '1':
                    for j in User.objects.all(): 
                        #si la caja a borrar esta abierta
                        # entonces que cambie el status a 2 
                        # si el usuario de caja a borrar es el mismo de la tabla user
                        if self.object.usuario_id == j.id:
                            j.status='2'
                            j.save()
                
                form = self.get_form()
                # cargo los valores de la fecha final - monto final - total de ventas de forma automatica
                c=form.save(commit=False)
                for i in Sale.objects.all():
                    if i.date_joined.strftime('%Y-%m-%d') == request.user.last_login.strftime('%Y-%m-%d') and request.user.id == i.usuario_id:
                        print("entro al if")
                        monto_finals = monto_finals + i.total  
                        total_ventas = total_ventas + 1      
                for i in Caja.objects.all():
                    if i.status == '1': 
                        i.fecha_cierre = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        i.monto_final = monto_finals - i.monto_inicial
                        i.total_venta = total_ventas
                        i.status = 2
                        i.save()
                # c.monto_final=
                # c.total_venta=
                # data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Cerrar caja'
        context['list_url'] = reverse_lazy("Caja:agregar_cajas")
        context['action'] = 'edit'
        context['entity'] = 'Caja'
        return context

