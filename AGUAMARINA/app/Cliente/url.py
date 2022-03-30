from django.contrib import admin
from django.urls import path

from Cliente.views import *

urlpatterns = [
    path('lista/', ClienteListview.as_view(), name='Listado de clientes'),
    path('crear/', ClienteCreateView.as_view(), name='Agregar clientes'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='Editar clientes'),
    path('eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='Eliminar clientes'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
