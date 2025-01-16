from django.db import models
from Apps.Catalogos.generos.models import GeneroModel

class PacienteModel(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=16, null=True, blank=True)
    nombre = models.CharField(max_length=60, null=False, blank=False)
    edad = models.CharField(max_length=2, null=False, blank=False)
    genero = models.ForeignKey(GeneroModel, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    ocupacion = models.CharField(max_length=30, null=False, blank=False)
    antecedentes = models.CharField(max_length=30, null=False, blank=False)
    isdeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbPaciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

