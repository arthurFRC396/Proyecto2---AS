from django.contrib import admin
from django.urls import path

from Compra.views import *

urlpatterns = [
    path('lista/', CompraListview.as_view(), name='Listado de compras'),
    path('crear/', CompraCreateView.as_view(), name='Agregar compra'),
    # path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='Editar clientes'),
    path('eliminar/<int:pk>/', CompraDeleteView.as_view(), name='Eliminar compra'),
    # home
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
