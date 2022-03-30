from django.urls import path

from Producto.views import *

urlpatterns = [
    path('lista_tipo_producto/', TipoProductoListview.as_view(), name='Listado Tipos De Producto'),
    path('crear_tipo_producto/', TipoProductoCreateView.as_view(), name='Agregar Tipo De Producto'),
    path('editar_tipo_producto/<int:pk>/', TipoProductoUpdateView.as_view(), name='Editar Tipo De Producto'),
    path('eliminar_tipo_producto/<int:pk>/', TipoProductoDeleteView.as_view(), name='Eliminar Tipo De Producto'),
    # url producto
    path('lista_producto/', ProductoListview.as_view(), name='Listado De Producto'),
    path('crear_producto/', ProductoCreateView.as_view(), name='Agregar Producto'),
    path('editar_producto/<int:pk>/', ProductoUpdateView.as_view(), name='Editar Producto'),
    path('eliminar_producto/<int:pk>/', ProductoDeleteView.as_view(), name='Eliminar Producto'),
    # url oferta
    path('lista_oferta/', OfertaListview.as_view(), name='Listado De Oferta'),
    path('crear_oferta/', OfertaCreateView.as_view(), name='Agregar Oferta'),
    path('editar_oferta/<int:pk>/', OfertaUpdateView.as_view(), name='Editar Oferta'),
    path('eliminar_oferta/<int:pk>/', OfertaDeleteView.as_view(), name='Eliminar Oferta'),


]
