from django.contrib import admin
from django.urls import path

from Compra.views import *

urlpatterns = [
    path('lista/', CompraListview.as_view(), name='Listado de compras'),
    path('crear/', CompraCreateView.as_view(), name='Agregar compra'),
    path('editar/<int:pk>/', CompraUpdateView.as_view(), name='Editar Compra'),
    path('eliminar/<int:pk>/', CompraDeleteView.as_view(), name='Eliminar compra'),
    path('pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='compra_invoice_pdf'),
    path('lista Nota/', NotaCompraListview.as_view(), name='Listado de Nota Credito Compra'),
    path('Nota/', NotaCreditoProveedorCreateView.as_view(), name='Agregar Nota Credito Compra'),
    path('eliminar nota/<int:pk>/', NotaCreditoProveedorDeleteView.as_view(), name='Eliminar Nota Compra'),

    # home
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
