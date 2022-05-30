from django.contrib import admin
from django.urls import path

from Caja.views import *

app_name = 'Caja'
urlpatterns = [
    path('lista/', CajaListview.as_view(), name='listar_cajas'),
    path('crear/', CajaCreateView.as_view(), name='agregar_cajas'),
    path('editar/<int:pk>/', CajaUpdateView.as_view(), name='editar_cajas'),
    path('eliminar/<int:pk>/', CajaDeleteView.as_view(), name='eliminar_cajas'),
    path('cerrar/<int:pk>/', CajaCerrarView.as_view(), name='cerrar_cajas'),

]
