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
from .serializer import EstadoPagoSerializer
from .models import EstadoPagoModel
from ...Seguridad.permissions import CustomPermission

class EstadoPagoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadoPagoModel

    @swagger_auto_schema(
        responses={200: EstadoPagoSerializer(many=True)}
    )
    def get(self, request):
        try:
            estados = EstadoPagoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            estado_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if estado_id and not estado_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if estado_id:
                estados = estados.filter(id=estado_id)
            if nombre:
                estados = estados.filter(nombre__icontains=nombre)

            serializer = EstadoPagoSerializer(estados, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {estados.count()} estados.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los estadosPago: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)