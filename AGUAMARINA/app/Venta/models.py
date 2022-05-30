from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import model_to_dict

from Cliente.models import Cliente
from Producto.models import Producto
from Venta.choices import pago_choices
from user.models import User


class Sale(models.Model):
    cli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.FloatField(default=0.00)
    es_procesado = models.CharField(default='N', max_length=1, verbose_name='procesado')
        # models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    pago = models.CharField(max_length=40, choices=pago_choices, default='efectivo')

    def __str__(self):
        return self.cli.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['usuario'] = self.usuario.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.FloatField(default=0.00)
        # models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        #return self.prod.nombre
        return  str(self.id).zfill(6)

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']


class NotaCreditoVenta(models.Model):
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
        verbose_name = 'Nota Credito Venta'
        verbose_name_plural = 'Notas Credito Ventas'
        ordering = ['id']

class DetNotaCreditoVenta(models.Model):
    detventa_datos = models.ForeignKey(DetSale, on_delete=models.CASCADE)
    notacredito = models.ForeignKey(NotaCreditoVenta, on_delete=models.CASCADE)
    cantnota = models.IntegerField(default=0)
    totalnota = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    desc = models.CharField(max_length=150, null=True, blank=True, verbose_name='desc')

    def __str__(self):
        return  self.id


    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = self.detventa_datos.prod.toJSON()
        item['price'] = format(self.detventa_datos.price, '.2f')
        item['totalnota'] = format(self.totalnota, '.2f')
        item['detventa_datos_id'] = str(self.detventa_datos_id).zfill(6)
        return item

    class Meta:
        verbose_name = 'Detalle de Nota Credito Venta'
        verbose_name_plural = 'Detalles de Nota Credito Venta'
        ordering = ['id']