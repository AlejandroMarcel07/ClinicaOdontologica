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
from .serializer import ExploracionSerializer
from .models import ExploracionModel
from ...Seguridad.permissions import CustomPermission

class ExploracionApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = ExploracionModel

    @swagger_auto_schema(
        responses={200: ExploracionSerializer(many=True)}
    )
    def get(self, request):
        try:
            exploraciones = ExploracionModel.objects.all()

            #Verificar que haigan parametros para filtrar
            exploracion_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if exploracion_id and not exploracion_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if exploracion_id:
                exploraciones = exploraciones.filter(id=exploracion_id)
            if nombre:
                exploraciones = exploraciones.filter(nombre__icontains=nombre)

            serializer = ExploracionSerializer(exploraciones, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {exploraciones.count()} exploraciones.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los generos: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)