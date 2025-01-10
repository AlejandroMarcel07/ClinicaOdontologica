from rest_framework import serializers
from .models import MontoDescuentoModel




class MontoDescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MontoDescuentoModel
        fields = ['id', 'cantidad']

    def validate_cantidad(self, value):
        """ Valida que el valor este en el rango correcto"""
        if value < 0 or value >= 100:
            raise serializers.ValidationError(
                {'Cantidad': 'El campo debe ser un valor valido.'}
            )
        return value




