# Generated by Django 4.2 on 2025-01-14 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiposPago', '0003_alter_tipopagomodel_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipopagomodel',
            name='nombre',
            field=models.CharField(default=0, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
