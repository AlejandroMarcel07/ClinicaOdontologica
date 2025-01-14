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
from .serializer import ModalidadPagoSerializer
from .models import ModalidadPagoModel
from ...Seguridad.permissions import CustomPermission

class ModalidadPagoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = ModalidadPagoModel

    @swagger_auto_schema(
        responses={200: ModalidadPagoSerializer(many=True)}
    )
    def get(self, request):
        try:
            modelos = ModalidadPagoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            modelos_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if modelos_id and not modelos_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if modelos_id:
                modelos = modelos.filter(id=modelos_id)
            if nombre:
                modelos = modelos.filter(nombre__icontains=nombre)

            serializer = ModalidadPagoSerializer(modelos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {modelos.count()} modalidades.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar las modalidades: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)