from django.contrib import admin
from django.urls import path

from Venta.views import *

urlpatterns = [
    path('lista/', SaleListView.as_view(), name='Listado de Venta'),
    path('crear/', SaleCreateView.as_view(), name='Agregar Venta'),
    path('editar/<int:pk>/', SaleUpdateView.as_view(), name='Editar Venta'),
    path('eliminar/<int:pk>/', SaleDeleteView.as_view(), name='Eliminar Venta'),
    path('pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    path('listaNota/', NotaVentaListview.as_view(), name='Listado de Nota Credito Venta'),
    path('Nota/', NotaCreditoVentaCreateView.as_view(), name='Agregar Nota Credito Venta'),
    path('Grafico/', dashventaview.as_view(), name='Grafico Venta'),
    #path('eliminar nota/<int:pk>/', NotaCreditoProveedorDeleteView.as_view(), name='Eliminar Nota Compra'),
    # # home
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
