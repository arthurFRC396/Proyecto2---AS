from django.contrib import admin
from django.urls import path

from Venta.views import *

urlpatterns = [
    path('lista/', SaleListView.as_view(), name='Listado de Venta'),
    path('crear/', SaleCreateView.as_view(), name='Agregar Venta'),
    path('editar/<int:pk>/', SaleUpdateView.as_view(), name='Editar Venta'),
    path('eliminar/<int:pk>/', SaleDeleteView.as_view(), name='Eliminar Venta'),
    path('pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # # home
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
