from django.contrib import admin
from django.urls import path, include
from homepage.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Login.urls')),
    path('cliente/', include('Cliente.url')),
    path('producto/', include('Producto.url')),
    path('vendedor/', include('vendedor.urls')),
    path('proveedor/', include('Proveedor.url')),
    path('usuario/', include('user.urls')),
    path('Venta/', include('Venta.url')),
    path('Compra/', include('Compra.url')),
    path('Caja/', include('Caja.url')),
]
