from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.forms import model_to_dict
from Producto.models import Producto
from Proveedor.models import Proveedor
from Venta.choices import compra_choices


class Compra(models.Model):
    prov_datos = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    stock_actual = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='stock actual', default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    precio_unitario = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    pago = models.CharField(max_length=40, choices=compra_choices, default='efectivo')
    fecha_compra = models.DateField(default=datetime.now)
    fecha_vencimiento = models.DateField(default=datetime.now)

    def __str__(self):
        return self.prov_datos.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['prov_datos'] = self.prov_datos.toJSON()
        item['total'] = format(self.total, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['fecha_compra'] = self.fecha_compra.strftime('%Y-%m-%d')
        item['fecha_vencimiento'] = self.fecha_vencimiento.strftime('%Y-%m-%d')
        # item['prov_datos'] = [i.toJSON() for i in self.objects.all()]
        item['det'] = [i.toJSON() for i in self.detcompra_set.all()]
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']


class DetCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['compra'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        ordering = ['id']
