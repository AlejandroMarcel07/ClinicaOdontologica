#IMPORTACIONES 1
from http.client import responses
from django.db import DatabaseError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
import logging
# Configura el logger
logger = logging.getLogger(__name__)
#IMPORTACIONES 2
from .serializer import PacienteSerializer
from .models import PacienteModel
from ...Seguridad.permissions import CustomPermission

class PacienteApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = PacienteModel

    @swagger_auto_schema(
        responses={200: PacienteSerializer(many=True)}
    )
    def get(self, request):
        try:
            pacientes = PacienteModel.objects.all()

            #Verificar que haigan parametros para filtrar
            paciente_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if paciente_id and not paciente_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if paciente_id:
                pacientes = pacientes.filter(id=paciente_id)
            if nombre:
                pacientes = pacientes.filter(nombre__icontains=nombre)

            serializer = PacienteSerializer(pacientes, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {pacientes.count()} pacientes.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los pacientes: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
