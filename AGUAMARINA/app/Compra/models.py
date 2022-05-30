from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.forms import model_to_dict
from Producto.models import Producto
from Proveedor.models import Proveedor
from Venta.choices import compra_choices,compra_cuota_choices


class Compra(models.Model):
    prov_datos = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    stock_actual = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='stock actual', default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    precio_unitario = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    pago = models.CharField(max_length=40, choices=compra_choices, default='Contado')
    fecha_compra = models.DateField(default=datetime.now)
    fecha_vencimiento = models.DateField(default=datetime.now)
    cant_cuota = models.IntegerField(default=0, choices=compra_cuota_choices)
    desc = models.CharField(max_length=150, null=True, blank=True, verbose_name='desc')
    es_procesado = models.CharField(default='N', max_length=1, verbose_name='procesado')
    fecha_emision_nota = models.DateField(default=datetime.now)


    def __str__(self):
        return self.prov_datos.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['prov_datos'] = self.prov_datos.toJSON()
        item['total'] = format(self.total, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['fecha_compra'] = self.fecha_compra.strftime('%Y-%m-%d')
        item['fecha_vencimiento'] = self.fecha_vencimiento.strftime('%Y-%m-%d')
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
    desc = models.CharField(max_length=150, null=True, blank=True, verbose_name='desc')

    def __str__(self):
        #return '{} {} / {}'.format(self.prod.nombre, str(self.compra_id).zfill(6))
        #return  self.prod.nombre
        return  str(self.id).zfill(6)


    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        ordering = ['id']


class NotaCreditoCompra(models.Model):
    desc_nota = models.CharField(max_length=150, null=True, blank=True, verbose_name='desc')
    fecha_emision_nota = models.DateField(default=datetime.now)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    nro_factura = models.IntegerField(default=0)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id).zfill(6)

    def toJSON(self):
        item = model_to_dict(self)
        item['desc_nota'] = self.desc_nota
        return item

    class Meta:
        verbose_name = 'Nota Credito Proveedor'
        verbose_name_plural = 'Notas Credito Proveedores'
        ordering = ['id']

class DetNotaCreditoCompra(models.Model):
    detcompra_datos = models.ForeignKey(DetCompra, on_delete=models.CASCADE)
    notacredito = models.ForeignKey(NotaCreditoCompra, on_delete=models.CASCADE)
    cantnota = models.IntegerField(default=0)
    totalnota = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    desc = models.CharField(max_length=150, null=True, blank=True, verbose_name='desc')

    def __str__(self):
        return  self.id


    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = self.detcompra_datos.prod.toJSON()
        item['price'] = format(self.detcompra_datos.price, '.2f')
        item['totalnota'] = format(self.totalnota, '.2f')
        item['detcompra_datos_id'] = str(self.detcompra_datos_id).zfill(6)
        return item

    class Meta:
        verbose_name = 'Detalle de Nota Credito Compra'
        verbose_name_plural = 'Detalles de Nota Credito Compra'
        ordering = ['id']