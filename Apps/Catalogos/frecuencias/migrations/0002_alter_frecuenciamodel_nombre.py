# Generated by Django 4.2 on 2025-01-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frecuencias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frecuenciamodel',
            name='nombre',
            field=models.CharField(default=0, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
