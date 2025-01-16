from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from Apps.Movimientos.clinicas.models import ClinicaModel


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    clinica = serializers.PrimaryKeyRelatedField(queryset=ClinicaModel.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'clinica')

    # Validar que ambas contraseñas coincidan
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    # Crear el usuario
    def create(self, validated_data):
        clinica = validated_data.pop('clinica', None)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            clinica=clinica
        )
        user.set_password(validated_data['password'])  # Encriptar la contraseña
        user.save()
        return user