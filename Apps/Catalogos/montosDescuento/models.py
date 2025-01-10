from django.core.exceptions import ValidationError
from django.db import models

def validar_descuento(value):
    """
    Valida que el valor ingresado se un numero decimal positivo y no tenga espacios ni caracteres invalidos
    """
    try:
        if value < 0 or value>= 100:
            raise ValidationError('El valor de descuento debe estar entre 0 y 100(excluyendo ambos).')
    except TypeError:
        raise ValidationError('El valor del descuento debe de ser un numero decimal valido.')


class MontoDescuentoModel(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, unique=True, validators=[validar_descuento])

    def save(self, *args, **kwargs):
        if self.cantidad is not None:
            self.cantidad = round(self.cantidad, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad}%'

    class Meta:
        db_table = 'TbMontoDescuento'
        verbose_name = 'MontoDescuento'
        verbose_name_plural = 'MontosDescuento'
