# Generated by Django 4.0.3 on 2022-05-29 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0007_inventario_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
