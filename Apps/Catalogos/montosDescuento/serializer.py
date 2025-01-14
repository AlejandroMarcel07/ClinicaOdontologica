from rest_framework import serializers
from .models import MontoDescuentoModel

def validate_unique(value):
    if MontoDescuentoModel.objects.filter(cantidad=value).exists():
        raise serializers.ValidationError("¡Esta cantidad ya existe!")
    return value

class MontoDescuentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MontoDescuentoModel
        fields = ['id', 'cantidad']
        extra_kwargs = {
            'cantidad': {
                'error_messages':{
                    'invalid':'¡Ingresa una cantidad valida!',
                    'max_value': '¡La cantidad no puede ser mayor que 100!',
                    'min_value': '¡La cantidad no puede ser menor que 0!'
                },
                'validators': [validate_unique]
            }
        }






