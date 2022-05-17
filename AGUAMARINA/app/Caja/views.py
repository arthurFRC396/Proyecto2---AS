
from datetime import datetime
from Caja.forms import CajaForm
from Caja.models import Caja
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView

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
        try:
            action = request.POST['action']
            if action == 'edit': 
                 
                
                form = self.get_form()
                # cargo los valores de la fecha final - monto final - total de ventas de forma automatica
                c=form.save(commit=False)
                for i in Caja.objects.all():
                    print("entro al for") 
                    if i.status=='1':
                        print(i.id) 
                        i.fecha_cierre=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(i.fecha_cierre)
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
        context['title'] = ' Editar caja'
        context['list_url'] = reverse_lazy("Caja:listar_cajas")
        context['action'] = 'edit'
        context['entity'] = 'Caja'
        return context

