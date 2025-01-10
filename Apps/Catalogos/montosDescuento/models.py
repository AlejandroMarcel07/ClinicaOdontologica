from django.db import models

class MontoDescuentoModel(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad}%'

    class Meta:
        db_table = 'TbMontoDescuento'
        verbose_name = 'MontoDescuento'
        verbose_name_plural = 'MontosDescuento'
