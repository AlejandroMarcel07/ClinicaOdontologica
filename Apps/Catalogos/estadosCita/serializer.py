from rest_framework import serializers
from .models import EstadoCitaModel

def validate_name(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise serializers.ValidationError("¡El nombre no debe contener simbolos ni numeros!")
    return value

def validate_uniquename(value):
    if EstadoCitaModel.objects.filter(nombre__iexact=value).exists():
        raise serializers.ValidationError("¡Este estado de cita ya existe!.")
    return value


class EstadoCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCitaModel
        fields =['id','nombre']
        extra_kwargs = {
            'nombre': {
                'error_messages':{
                    'invalid':'¡Ingresa un estado de cita valido!',
                    'blank':'¡El campo no puede estar vacio!',
                    'max_length':'¡Superaste la cantidad de caracteres!'
                },
                'validators': [validate_name, validate_uniquename]
            }
        }