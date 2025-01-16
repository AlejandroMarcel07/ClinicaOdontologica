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


    @swagger_auto_schema(
        request_body=EstadoFechaSerializer, responses={201: EstadoFechaSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = EstadoFechaSerializer(data=data)

            if serializer.is_valid():
                estado = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo Estado de fecha con id: '{estado.id}'"
                )
                return Response(
                    {
                        "message": "Estado fecha creado exitosamente.",
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
        request_body=EstadoFechaSerializer, responses={200: EstadoFechaSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                estado = EstadoFechaModel.objects.get(id=id)
            except EstadoFechaModel.DoesNotExist:
                logger.warning(f"El Estado de fecha con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado de fecha con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = EstadoFechaSerializer(estado, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo el Estado de fecha con id {id}")
                return Response(
                    {
                        "message": "Estado Fecha actualizado exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar el Estado de fecha con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                estado = EstadoFechaSerializer.objects.get(id=id)
            except EstadoFechaModel.DoesNotExist:
                logger.warning(f"El Estado de fecha con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado de fecha con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, estado)
            estado.delete()

            logger.info(f"El usuario '{request.user}' elimino el Estado de fecha con id: {id}")
            return Response(
                {"message": f"El Estado de fecha con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el Estado de fecha con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )