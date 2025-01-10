from rest_framework import serializers
from .models import MontoDescuentoModel

class MontoDescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MontoDescuentoModel
        fields = ['id', 'cantidad']
        extra_kwargs = {
            'cantidad': {
                'required': True,
                'error_messages': {
                    'required': 'El campo cantidad es obligatorio.',
                    'blank': 'El campo cantidad no puede estar vacío.',
                    'invalid': 'Debe ingresar un valor numérico válido para el descuento.',
                }
            }
        }
