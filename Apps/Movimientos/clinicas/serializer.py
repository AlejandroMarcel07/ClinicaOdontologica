from rest_framework import serializers
from .models import ClinicaModel


class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicaModel
        fields =['id','nombre', 'direccion', 'telefono', 'encargado']