from django.core.exceptions import ValidationError
from django.db import models

def validar_nombre(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError('El nombre no debe contener simbolos ni numeros.')

class FrecuenciaModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10, null=True, blank=False, unique=True, validators=[validar_nombre])

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbFrecuencia'
        verbose_name = 'Frecuencia'
        verbose_name_plural = 'Frecuencias'