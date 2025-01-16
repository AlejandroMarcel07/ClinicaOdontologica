from rest_framework import serializers
from .models import PacienteModel

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteModel
        fields = '__all__'