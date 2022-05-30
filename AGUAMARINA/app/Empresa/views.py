
from Empresa.forms import EmpresaForm,EmpresaupdateForm
from Empresa.models import Empresa
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView

class EmpresaListview(ListView):
    model = Empresa
    template_name = 'lista_empresa.html'

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
                for i in Empresa.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Empresas'
        context['boton'] = 'Empresa'
        context['create_url'] = reverse_lazy("Agregar Empresas")
        context['list_url'] = reverse_lazy("Listado de Empresas")
        context['entity'] = 'Empresa'
        return context

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'create_empresa.html'
    success_url = reverse_lazy("Listado de Empresas")

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
        context['title'] = ' Agregar Empresa'
        context['list_url'] = reverse_lazy("Listado de Empresas")
        context['action'] = 'add'
        context['entity'] = 'Empresa'
        return context


class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaupdateForm
    template_name = 'create_empresa.html'
    success_url = reverse_lazy("Listado de Empresas")

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
        context['title'] = ' Editar Empresa'
        context['list_url'] = reverse_lazy("Listado de Empresas")
        context['action'] = 'edit'
        context['entity'] = 'Empresa'
        return context


class EmpresaDeleteView(DeleteView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'delete_empresa.html'
    success_url = reverse_lazy("Listado de Empresas")

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Eliminar Empresa'
        context['list_url'] = reverse_lazy("Listado de Empresas")
        context['entity'] = 'Empresa'
        return context
