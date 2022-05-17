from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from Caja.choices import status_choices
from user.models import User



class Caja(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=datetime.now, verbose_name='Fecha de inicio')
    fecha_cierre = models.DateTimeField(default=datetime.now, verbose_name='Fecha de cierre', null=True)
    monto_inicial = models.IntegerField(verbose_name='Monto inicial')
    monto_final = models.IntegerField(verbose_name='Monto final', null=True)
    total_venta = models.IntegerField(verbose_name='Total de ventas', null=True)
    status = models.CharField(max_length=10, choices=status_choices, default='1', verbose_name='status')
    

    def __str__(self):
        return '{} {}'.format("Caja-numero:", str(self.id))

    # def get_full_name(self):
    #     return '{} {} / {}'.format(self.nombre, self.apellido)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'
        db_table = 'Caja'
        ordering = ['id']
