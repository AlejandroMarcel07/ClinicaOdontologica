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
from .serializer import ClinicaSerializer
from .models import ClinicaModel
from ...Seguridad.permissions import CustomPermission

class ClinicaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = ClinicaModel

    @swagger_auto_schema(
        responses={200: ClinicaSerializer(many=True)}
    )
    def get(self, request):
        try:
            clinicas = ClinicaModel.objects.all()

            #Verificar que haigan parametros para filtrar
            clinica_id = request.query_params.get('id', None)

            #Validar
            if clinica_id and not clinica_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if clinica_id:
                clinicas = clinicas.filter(id=clinica_id)

            serializer = ClinicaSerializer(clinicas, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {clinicas.count()} clinicas.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar las clinicas: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)