# Generated by Django 4.0.3 on 2022-05-19 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0002_alter_inventario_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='permisos_inventario'),
        ),
    ]
