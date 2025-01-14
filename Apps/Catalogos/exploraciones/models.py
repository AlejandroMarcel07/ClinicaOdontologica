from django.core.exceptions import ValidationError
from django.db import models


class ExploracionModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TbExploracion'
        verbose_name = 'Exploracion'
        verbose_name_plural = 'Exploraciones'
