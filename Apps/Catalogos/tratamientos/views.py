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
from .serializer import TratamientoSerializer
from .models import TratamientoModel
from ...Seguridad.permissions import CustomPermission

class TratamientoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TratamientoModel

    @swagger_auto_schema(
        responses={200: TratamientoSerializer(many=True)}
    )
    def get(self, request):
        try:
            tratamientos = TratamientoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            tratamiento_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if tratamiento_id and not tratamiento_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if tratamiento_id:
                tratamientos = tratamientos.filter(id=tratamiento_id)
            if nombre:
                tratamientos = tratamientos.filter(nombre__icontains=nombre)

            serializer = TratamientoSerializer(tratamientos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {tratamientos.count()} tratamientos.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los generos: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)