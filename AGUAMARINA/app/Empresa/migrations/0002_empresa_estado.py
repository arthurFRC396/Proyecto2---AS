# Generated by Django 4.0.3 on 2022-05-22 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='estado',
            field=models.CharField(default='A', max_length=1),
        ),
    ]