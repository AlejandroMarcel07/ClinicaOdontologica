from django.core.exceptions import ValidationError
from django.db import models

def validar_nombre(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError('El nombre no debe contener simbolos ni numeros.')

class EstadoCuentaModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, null=True, blank=False, unique=True, validators=[validar_nombre])

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbEstadoCuenta'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'