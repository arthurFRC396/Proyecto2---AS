
from Cliente.forms import ClienteForm
from Cliente.models import Cliente
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView

class ClienteListview(ListView):
    model = Cliente
    template_name = 'lista_cliente.html'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de clientes'
        context['boton'] = 'Cliente'
        context['create_url'] = reverse_lazy("Agregar clientes")
        context['list_url'] = reverse_lazy("Listado de clientes")
        context['entity'] = 'Cliente'
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'create_cliente.html'
    success_url = reverse_lazy("Listado de clientes")

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
        context['title'] = ' Agregar cliente'
        context['list_url'] = reverse_lazy("Listado de clientes")
        context['action'] = 'add'
        context['entity'] = 'Cliente'
        return context


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'create_cliente.html'
    success_url = reverse_lazy("Listado de clientes")

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
        context['title'] = ' Editar cliente'
        context['list_url'] = reverse_lazy("Listado de clientes")
        context['action'] = 'edit'
        context['entity'] = 'Cliente'
        return context


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'delete_cliente.html'
    success_url = reverse_lazy("Listado de clientes")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         self.object.delete()
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Cliente'
        context['list_url'] = reverse_lazy("Listado de clientes")
        context['entity'] = 'Cliente'
        return context

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        return context
