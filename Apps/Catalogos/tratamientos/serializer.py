from rest_framework import serializers
from .models import TratamientoModel

class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TratamientoModel
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