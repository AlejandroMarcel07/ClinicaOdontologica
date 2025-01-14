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
from .serializer import GeneroSerializer
from .models import GeneroModel
from ...Seguridad.permissions import CustomPermission


class GeneroApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = GeneroModel

    @swagger_auto_schema(
        responses={200: GeneroSerializer(many=True)}
    )
    def get(self, request):
        try:
            generos = GeneroModel.objects.all()

            #Verificar que haigan parametros para filtrar
            genero_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if genero_id and not genero_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if genero_id:
                generos = generos.filter(id=genero_id)
            if nombre:
                generos = generos.filter(nombre__icontains=nombre)

            serializer = GeneroSerializer(generos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {generos.count()} generos.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los generos: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


