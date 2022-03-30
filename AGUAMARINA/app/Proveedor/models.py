from datetime import datetime
from django.db import models
from django.forms import model_to_dict


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    ruc = models.CharField(max_length=150, verbose_name='Ruc', unique=True)
    direccion = models.CharField(max_length=300, verbose_name='Direccion')
    correo = models.CharField(max_length=400, verbose_name='E-Mail')
    telefono = models.CharField(max_length=300, verbose_name='Telefono', default='')
    ingresado = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        # item['nombre'] = '{} / {}'.format(self.nombre, self.tipo_producto.nombre)
        item['nombre'] = self.nombre
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'
        ordering = ['id']
