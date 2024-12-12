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
from .serializer import TipoPagoSerializer
from .models import TipoPagoModel
from ...Seguridad.permissions import CustomPermission

class TipoPagoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoPagoModel


    @swagger_auto_schema(
        responses={200: TipoPagoSerializer(many=True)}
    )

    def get(self, request):
        try:
            tipos = TipoPagoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            tipo_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if tipo_id and not tipo_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if tipo_id:
                tipos = tipos.filter(id=tipo_id)
            if nombre:
                tipos = tipos.filter(nombre__icontains=nombre)

            serializer = TipoPagoSerializer(tipos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {tipos.count()} tipos de pago.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los tipos de pago: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)