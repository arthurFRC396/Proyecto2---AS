from django.contrib import admin
from django.urls import path

from Proveedor.views import *

urlpatterns = [
    path('lista/', ProveedorListview.as_view(), name='Listado de proveedores'),
    path('crear/', ProveedorCreateView.as_view(), name='Agregar proveedor'),
    path('editar/<int:pk>/', ProveedorUpdateView.as_view(), name='Editar proveedor'),
    path('eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='Eliminar proveedor'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
