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

    @swagger_auto_schema(
        request_body=MontoDescuentoSerializer, responses={201: MontoDescuentoSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = MontoDescuentoSerializer(data=data)

            if serializer.is_valid():
                monto_descuento = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo monto de descuento con id: '{monto_descuento.id}'"
                )
                return Response(
                    {
                        "message": "Monto de descuento creado exitosamente.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                logger.warning(f"Errores de validación: {serializer.errors}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            # Registra errores en el servidor
            logger.error(f"Error interno del servidor: {str(e)}")
            return Response(
                {
                    "error": "Error interno del servidor. Por favor, inténtelo de nuevo más tarde."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        request_body=MontoDescuentoSerializer, responses={200: MontoDescuentoSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                montodescuento = MontoDescuentoModel.objects.get(id=id)
            except MontoDescuentoModel.DoesNotExist:
                logger.warning(f"El monto de descuento con id {id} no existe.")
                return  Response(
                    {"error": f"El Estado cita con id {id} no existe"},
                    status = status.HTTP_404_NOT_FOUND
                )
            serializer = MontoDescuentoSerializer(montodescuento, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.data}' actualizo el monto de descuento con id {id}")
                return Response(
                    {
                        "message": "Monto de descuento actualizado exitosamente.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                logger.warning(f"Errores de validación: {serializer.errors}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.error(f"Error interno del servidor al actualizar el monto de descuento con id {id}: {str(e)}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )