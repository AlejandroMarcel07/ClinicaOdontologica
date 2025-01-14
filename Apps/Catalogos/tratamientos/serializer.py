from rest_framework import serializers
from .models import TratamientoModel

def validate_name(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise serializers.ValidationError("¡El nombre no debe contener simbolos ni numeros!")
    return value

def validate_uniquename(value):
    if TratamientoModel.objects.filter(nombre__iexact=value).exists():
        raise serializers.ValidationError("¡Este tratamiento ya existe!.")
    return value

class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TratamientoModel
        fields =['id','nombre']
        extra_kwargs = {
            'nombre': {
                'error_messages':{
                    'invalid':'¡Ingresa un tratamiento valido!',
                    'blank':'¡El campo no puede estar vacio!',
                    'max_length':'¡Superaste la cantidad de caracteres!'
                },
                'validators': [validate_name, validate_uniquename]
            }
        }