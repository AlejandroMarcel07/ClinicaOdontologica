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
            modalidades = ModalidadPagoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            modalidad_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if modalidad_id and not modalidad_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if modalidad_id:
                modalidades = modalidades.filter(id=modalidad_id)
            if nombre:
                modalidades = modalidades.filter(nombre__icontains=nombre)

            serializer = ModalidadPagoSerializer(modalidades, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {modalidades.count()} modalidades de pago.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar las modalidades: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)