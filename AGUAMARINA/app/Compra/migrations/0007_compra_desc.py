# Generated by Django 4.0.3 on 2022-04-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compra', '0006_notacreditocompra_fecha_emision_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='desc',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='desc'),
        ),
    ]
