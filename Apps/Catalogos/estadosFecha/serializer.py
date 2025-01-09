from rest_framework import serializers
from .models import EstadoFechaModel

class EstadoFechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoFechaModel
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