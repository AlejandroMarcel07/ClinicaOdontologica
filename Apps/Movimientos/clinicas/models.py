from django.db import models

class ClinicaModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    telefono = models.CharField(max_length=8, null=False, blank=False)
    encargado = models.CharField(max_length=50, null=False, blank=False)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbClinica'
        verbose_name = 'Clinica'
        verbose_name_plural = 'Clinicas'
