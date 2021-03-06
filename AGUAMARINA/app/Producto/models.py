from django.db import models
from datetime import datetime
from django.forms import model_to_dict
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
import Proveedor.models


class TipoProducto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    descripcion = models.CharField(max_length=150, verbose_name='Descripcion')
    ingresado = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Producto'
        verbose_name_plural = 'Tipos de Productos'
        db_table = 'tipoproducto'
        ordering = ['id']


class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, verbose_name='Tipo Producto')
    proveedor = models.ForeignKey(Proveedor.models.Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    marca = models.CharField(max_length=150, verbose_name='Marca')
    precio_costo = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Precio Costo')
    precio_venta = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Precio Venta')
    stock = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='stock', default=0)
    es_oferta = models.CharField(default='N', max_length=1, verbose_name='Oferta')
    descripcion = models.CharField(max_length=150, verbose_name='Descripcion')
    chk_oferta = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    ingresado = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')

    def __str__(self):
        return str(self.id)

    # def __int__(self):
    #     return self.id

    def toJSON(self):
        item = model_to_dict(self)
        # item['nombre'] = '{} / {}'.format(self.nombre, self.tipo_producto.nombre)
        item['nombre'] = self.nombre
        item['tipo_producto'] = self.tipo_producto.toJSON()
        item['proveedor'] = self.proveedor.toJSON()
        item['precio_venta'] = format(self.precio_venta, '.2f')
        item['ingresado'] = self.ingresado.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'producto'
        ordering = ['id']


class Oferta(models.Model):
    producto_cod = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto a ofertar')
    porcentaje_descuento = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)],
                                               verbose_name='Porcentaje de descuento')
    fecha_inicio_oferta = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin_oferta = models.DateField(verbose_name='Fecha de fin')
    ingresado = models.DateTimeField(default=datetime.now, verbose_name='Fecha de registro')

    def __str__(self):
        return str(self.producto_cod)

    # def __int__(self):
    #     return self.producto_cod

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
        db_table = 'oferta'
        ordering = ['id']


class Oferta_temp(models.Model):
    oferta_cod = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    porcentaje_descuento = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)],
                                               verbose_name='Porcentaje de descuento', null=True)
    chk_delete = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    ingresado = models.DateTimeField(verbose_name='Fecha de registro', null=True)

class FilesUploads(models.Model):
        file = models.FileField()

class Inventario(models.Model):
    #prov_datos = models.ForeignKey(Proveedor.models.Proveedor, on_delete=models.CASCADE, default = 0)
    stock_actual = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='stock actual', default=0)
    es_procesado = models.CharField(default='N', max_length=1, verbose_name='procesado')
    fecha_registro = models.DateField(default=datetime.now)
    autorizado_por = models.CharField(max_length=20, null=True, blank=True, verbose_name='autorizado_por')
    cant = models.IntegerField(default=0)
    #image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.id


    def toJSON(self):
        item = model_to_dict(self)
        #item['prov_datos'] = self.prov_datos.toJSON()
        item['det'] = [i.toJSON() for i in self.detinventario_set.all()]
        #item['image'] = self.get_image()
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['id']


class DetInventario(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=150, null=True, blank=True, verbose_name='motivo')
    cantprod = models.IntegerField(default=0)

    def __str__(self):
        return  str(self.prod_id).zfill(6)

    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Inventario'
        verbose_name_plural = 'Detalles de Inventario'
        ordering = ['id']
