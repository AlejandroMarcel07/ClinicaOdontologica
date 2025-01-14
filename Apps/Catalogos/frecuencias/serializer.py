from rest_framework import serializers
from .models import FrecuenciaModel

def validate_name(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise serializers.ValidationError("¡El nombre no debe contener simbolos ni numeros!")
    return value

def validate_uniquename(value):
    if FrecuenciaModel.objects.filter(nombre__iexact=value).exists():
        raise serializers.ValidationError("¡Esta Frecuencia ya existe!.")
    return value

class FrecuenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrecuenciaModel
        fields =['id','nombre']
        extra_kwargs = {
            'nombre': {
                'error_messages':{
                    'invalid':'¡Ingresa una frecuencia valida!',
                    'blank':'¡El campo no puede estar vacio!',
                    'max_length':'¡Superaste la cantidad de caracteres!'
                },
                'validators': [validate_name, validate_uniquename]
            }
        }