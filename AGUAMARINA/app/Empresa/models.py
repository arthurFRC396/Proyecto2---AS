from datetime import datetime
from django.db import models
from django.forms import model_to_dict
#from Cliente.choices import gender_choices


class Empresa(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Empresa')
    establecimiento = models.CharField(max_length=3, verbose_name='Establecimiento', default= '001')
    punto_expedicion = models.CharField(max_length=3, verbose_name='Punto de expedicion',default= '001')
    timbrado = models.IntegerField(verbose_name='Timbrado')
    ruc = models.CharField(max_length=150, verbose_name='Ruc')
    fecha_vencimiento = models.DateField(default=datetime.now, verbose_name='Fecha de validez')
    direccion = models.CharField(max_length=300, verbose_name='Direccion')
    telefono = models.CharField(max_length=300, verbose_name='Telefono', default='')
    correo = models.CharField(max_length=400, verbose_name='E-Mail')
    ingresado = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')
    estado = models.CharField(default='A', max_length=1) # Estado A= activo, I = inactivo

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.id

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
      #  item['gender'] = {'id': self.genero, 'name': self.get_gender_display()}
        # item['nombre'] = self.nombre
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'empresas'
        ordering = ['id']
