from django.db import models

from django.forms import model_to_dict

# Create your models here.
class Vendedor(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cedula = models.IntegerField(verbose_name='cedula', unique=True)
    direccion = models.CharField(max_length=150, verbose_name='dirección')
    telefono = models.CharField(max_length=150, verbose_name='teléfono', unique=True)
    desc = models.CharField(max_length=150, null=True, blank=True, verbose_name='desc')


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        #como se va llamar la aplicacion en el Vendedor de django singular
        verbose_name = 'Vendedor'
        #como se va llamar la aplicacion en el Vendedor de django plural
        verbose_name_plural = 'Vendedores'
        #como se va llamar la el modelo o la tabla en la base de datos
        db_table = 't_vendedor'
        #el orden que va seguir
        ordering = ['id']


