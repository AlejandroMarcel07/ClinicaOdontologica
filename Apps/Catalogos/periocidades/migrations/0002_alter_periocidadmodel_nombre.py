# Generated by Django 4.2 on 2025-01-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('periocidades', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periocidadmodel',
            name='nombre',
            field=models.CharField(default=0, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
