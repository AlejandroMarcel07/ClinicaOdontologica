from django.core.exceptions import ValidationError
from django.db import models

class EstadoPagoModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=12, null=False, blank=False, unique=True)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbEstadoPago'
        verbose_name = 'EstadoPago'
        verbose_name_plural = 'EstadosPago'
