# Generated by Django 4.2 on 2025-01-14 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estadosPago', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadopagomodel',
            name='nombre',
            field=models.CharField(default=0, max_length=12, unique=True),
            preserve_default=False,
        ),
    ]