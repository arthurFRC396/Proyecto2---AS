from vendedor.forms import AdminForm
from django.http.response import JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from vendedor.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

def admin_list(request):
    context = {
        'title':'Lista de vendedores',
        'categories' : Vendedor.objects.all()
    }
    return render(request, 'admin/list.html',context)

class AdminListView(ListView):
    model = Vendedor
    template_name = 'admin/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Vendedor.objects.get(pk=request.POST['id']).toJSON()

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de vendedores'
        context['create_url'] = reverse_lazy('admini:AdminCreateView')
        context['list_url'] = reverse_lazy('admini:AdminListView')
        context['entity'] = 'venta'
        return context

class AdminCreateView(CreateView):
    model = Vendedor
    form_class = AdminForm 
    template_name = 'admin/create.html'
    success_url = reverse_lazy('admini:AdminListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar un vendedor'
        context['entity'] = 'venta'
        context['list_url'] = reverse_lazy('admini:AdminListView')
        context['action'] = 'add'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'no ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
"""    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data( **kwargs)
        context['form']= form
        return render(request, self.template_name, context)
"""

class AdminUpdateView(UpdateView):
    model = Vendedor
    form_class = AdminForm 
    template_name = 'admin/create.html'
    success_url = reverse_lazy('admini:AdminListView')

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
                data['error'] = 'no ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        #print(self.object)
        #print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un vendedor'
        context['entity'] = 'venta'
        context['list_url'] = reverse_lazy('admini:AdminListView')
        context['action'] = 'edit'
        return context

class AdminDeleteView(DeleteView):
    model = Vendedor
    form_class = AdminForm 
    template_name = 'admin/delete.html'
    success_url = reverse_lazy('admini:AdminListView')

    #@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            print(request.POST)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        #print(self.object)
        #print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar un vendedor'
        context['entity'] = 'venta'
        context['list_url'] = reverse_lazy('admini:AdminListView')
        return context