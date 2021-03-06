# Generated by Django 4.0.3 on 2022-05-19 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Venta', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Producto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detsale',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.producto'),
        ),
        migrations.AddField(
            model_name='detsale',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Venta.sale'),
        ),
        migrations.AddField(
            model_name='detnotacreditoventa',
            name='detventa_datos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Venta.detsale'),
        ),
        migrations.AddField(
            model_name='detnotacreditoventa',
            name='notacredito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Venta.notacreditoventa'),
        ),
    ]
