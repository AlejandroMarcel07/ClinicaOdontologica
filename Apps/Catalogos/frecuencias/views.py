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
from .serializer import FrecuenciaSerializer
from .models import FrecuenciaModel
from ...Seguridad.permissions import CustomPermission

class FrecuenciaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = FrecuenciaModel

    @swagger_auto_schema(
        responses={200: FrecuenciaSerializer(many=True)}
    )
    def get(self, request):
        try:
            frecuencias = FrecuenciaModel.objects.all()

            #Verificar que haigan parametros para filtrar
            frecuencia_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if frecuencia_id and not frecuencia_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if frecuencia_id:
                frecuencias = frecuencias.filter(id=frecuencia_id)
            if nombre:
                frecuencias = frecuencias.filter(nombre__icontains=nombre)

            serializer = FrecuenciaSerializer(frecuencias, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {frecuencias.count()} frecuencias.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los generos: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
