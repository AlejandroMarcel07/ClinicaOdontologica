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
            estadopagos = EstadoPagoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            estado_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if estado_id and not estado_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if estado_id:
                estadopagos = estadopagos.filter(id=estado_id)
            if nombre:
                estadopagos = estadopagos.filter(nombre__icontains=nombre)

            serializer = EstadoPagoSerializer(estadopagos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {estadopagos.count()} estados de pago.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los estados de pago: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=EstadoPagoSerializer, responses={201: EstadoPagoSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = EstadoPagoSerializer(data=data)

            if serializer.is_valid():
                estado = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo Estado pago con id: '{estado.id}'"
                )
                return Response(
                    {
                        "message": "Estado pago creado exitosamente.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                logger.warning(f"Errores de validación: {serializer.errors}, usuario: {request.user}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            # Registra errores en el servidor
            logger.error(f"Error interno del servidor: {str(e)}, usuario: {request.user}")
            return Response(
                {
                    "error": "Error interno del servidor. Por favor, inténtelo de nuevo más tarde."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    @swagger_auto_schema(
        request_body=EstadoPagoSerializer, responses={200: EstadoPagoSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                estado = EstadoPagoModel.objects.get(id=id)
            except EstadoPagoModel.DoesNotExist:
                logger.warning(f"El Estado pago con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado pago con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = EstadoPagoSerializer(estado, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo el Estado pago con id {id}")
                return Response(
                    {
                        "message": "Estado pago actualizado exitosamente.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                logger.warning(f"Errores de validación: {serializer.errors}, usuario: {request.user}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            logger.error(f"Error interno del servidor al actualizar el estado pago con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                estado = EstadoPagoModel.objects.get(id=id)
            except EstadoPagoModel.DoesNotExist:
                logger.warning(f"El Estado pago con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado pago con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, estado)
            estado.delete()

            logger.info(f"El usuario '{request.user}' elimino el Estado pago con id: {id}")
            return Response(
                {"message": f"El Estado pago con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el Estado pago con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )