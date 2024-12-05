from rest_framework import serializers
from .models import GeneroModel

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneroModel
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
