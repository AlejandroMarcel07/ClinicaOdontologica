# Generated by Django 4.2 on 2024-12-02 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneroModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Género',
                'verbose_name_plural': 'Géneros',
                'db_table': 'TbGenero',
            },
        ),
    ]
