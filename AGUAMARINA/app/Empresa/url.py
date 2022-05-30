from django.contrib import admin
from django.urls import path

from Empresa.views import *

urlpatterns = [
    path('lista/', EmpresaListview.as_view(), name='Listado de Empresas'),
    path('crear/', EmpresaCreateView.as_view(), name='Agregar Empresas'),
    path('editar/<int:pk>/', EmpresaUpdateView.as_view(), name='Editar Empresas'),
    path('eliminar/<int:pk>/', EmpresaDeleteView.as_view(), name='Eliminar Empresas'),
    # home
    #path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
