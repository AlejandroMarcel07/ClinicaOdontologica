from django.core.exceptions import ValidationError
from django.db import models


class EstadoCitaModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=False, blank=False, unique=True)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbEstadoCita'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'