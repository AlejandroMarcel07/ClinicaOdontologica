# Generated by Django 4.2 on 2024-12-30 16:50

import Apps.Catalogos.estadosCita.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estadosCita', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadocitamodel',
            name='nombre',
            field=models.CharField(max_length=20, null=True, unique=True, validators=[Apps.Catalogos.estadosCita.models.validar_nombre]),
        ),
    ]
