from rest_framework import serializers
from .models import EstadoPagoModel

def validate_name(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise serializers.ValidationError("¡El nombre no debe contener simbolos ni numeros!")
    return value

def validate_uniquename(value):
    if EstadoPagoModel.objects.filter(nombre__iexact=value).exists():
        raise serializers.ValidationError("¡Este estado de pago ya existe!.")
    return value

class EstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPagoModel
        fields =['id','nombre']
        extra_kwargs = {
            'nombre': {
                'error_messages':{
                    'invalid':'¡Ingresa un estado de pago valido!',
                    'blank':'¡El campo no puede estar vacio!',
                    'max_length':'¡Superaste la cantidad de caracteres!'
                },
                'validators': [validate_name, validate_uniquename]
            }
        }