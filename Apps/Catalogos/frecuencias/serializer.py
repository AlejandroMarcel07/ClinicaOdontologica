from rest_framework import serializers
from .models import FrecuenciaModel

class FrecuenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrecuenciaModel
        fields =['id','nombre']
        extra_kwargs = {
            'nombre':{
                'required':True,
                'error_messages':{
                    'required': 'El campo nombre es obligatorio.',
                    'blank': 'El campo no puede estar vacio.'
                }
            }
        }