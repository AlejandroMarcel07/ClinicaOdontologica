# Generated by Django 4.2 on 2024-12-30 16:50

import Apps.Catalogos.estadosCuenta.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estadosCuenta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadocuentamodel',
            name='nombre',
            field=models.CharField(max_length=25, null=True, unique=True),
        ),
    ]
