#IMPORTACIONES 1
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
from .serializer import EstadoCuentaSerializer
from .models import EstadoCuentaModel
from ...Seguridad.permissions import CustomPermission

class EstadoCuentaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadoCuentaModel

    @swagger_auto_schema(
        responses={200: EstadoCuentaSerializer(many=True)}
    )
    def get(self, request):
        try:
            estados = EstadoCuentaModel.objects.all()

            # Verificar que haigan parametros para filtrar
            estados_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            # Validar
            if estados_id and not estados_id.isdigit():
                raise ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            # Filtrar por parametros
            if estados_id:
                estados = estados.filter(id=estados_id)
            if nombre:
                estados = estados.filter(nombre__icontains=nombre)

            serializer = EstadoCuentaSerializer(estados, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {estados.count()} estados de cuenta.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los estados de cuenta: {e}, usuario: {request.user}")
            return Response({"error": "Hubo un problema al recuperar los datos."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
