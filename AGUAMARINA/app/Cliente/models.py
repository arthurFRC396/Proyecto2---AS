from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from Cliente.choices import gender_choices


class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido = models.CharField(max_length=150, verbose_name='Apellidos')
    ci = models.IntegerField(verbose_name='Cedula', unique=True)
    genero = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    ruc = models.CharField(max_length=150, verbose_name='Ruc', unique=True)
    nacimiento = models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    direccion = models.CharField(max_length=300, verbose_name='Direccion')
    telefono = models.CharField(max_length=300, verbose_name='Telefono', default='')
    ingresado = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.nombre, self.apellido, self.ci)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
      #  item['gender'] = {'id': self.genero, 'name': self.get_gender_display()}
        # item['nombre'] = self.nombre
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        ordering = ['id']
