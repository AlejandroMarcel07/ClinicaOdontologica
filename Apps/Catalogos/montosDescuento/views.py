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
from .serializer import MontoDescuentoSerializer
from .models import MontoDescuentoModel
from ...Seguridad.permissions import CustomPermission

class MontoDescuentoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = MontoDescuentoModel

    @swagger_auto_schema(
        responses={200: MontoDescuentoSerializer(many=True)}
    )
    def get(self, request):
        try:
            montos = MontoDescuentoModel.objects.all()

            serializer = MontoDescuentoSerializer(montos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {montos.count()} montos.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los montos de descuento: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)