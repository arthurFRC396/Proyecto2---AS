# Generated by Django 4.0.3 on 2022-05-29 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0008_alter_inventario_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='file',
        ),
        migrations.AddField(
            model_name='inventario',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen'),
        ),
    ]