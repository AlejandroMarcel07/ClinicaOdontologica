from django.db import models
from django.contrib.auth.models import AbstractUser
from Apps.Movimientos.clinicas.models import ClinicaModel


class User(AbstractUser):
    clinica = models.ForeignKey(ClinicaModel, on_delete=models.SET_NULL, null=True, blank=True
)