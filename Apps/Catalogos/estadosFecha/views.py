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
from .serializer import EstadoFechaSerializer
from .models import EstadoFechaModel
from ...Seguridad.permissions import CustomPermission

class EstadoFechaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadoFechaModel

    @swagger_auto_schema(
        responses={200: EstadoFechaSerializer(many=True)}
    )
    def get(self, request):
        try:
            estados = EstadoFechaModel.objects.all()

            # Verificar que haigan parametros para filtrar
            estado_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            # Validar
            if estado_id and not estado_id.isdigit():
                raise ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            # Filtrar por parametros
            if estado_id:
                estados = estados.filter(id=estado_id)
            if nombre:
                estados = estados.filter(nombre__icontains=nombre)

            serializer = EstadoFechaSerializer(estados, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {estados.count()} estados de fecha.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los estados de fecha: {e}, usuario: {request.user}")
            return Response({"error": "Hubo un problema al recuperar los datos."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)