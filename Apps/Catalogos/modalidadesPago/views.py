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

    @swagger_auto_schema(
        request_body=ModalidadPagoSerializer, responses={201: ModalidadPagoSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = ModalidadPagoSerializer(data=data)

            if serializer.is_valid():
                modalidad = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó una nueva modalidad con id: '{modalidad.id}'"
                )
                return Response(
                    {
                        "message": "Modalidad creada exitosamente.",
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
        request_body=ModalidadPagoSerializer, responses={200: ModalidadPagoSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                modalidad = ModalidadPagoModel.objects.get(id=id)
            except ModalidadPagoModel.DoesNotExist:
                logger.warning(f"La modalidad con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"La modalidad con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ModalidadPagoSerializer(modalidad, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo la modalidad con id {id}")
                return Response(
                    {
                        "message": "Modalidad actualizada exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar la modalidad con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                modalidad = ModalidadPagoModel.objects.get(id=id)
            except ModalidadPagoModel.DoesNotExist:
                logger.warning(f"La modalidad con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"La modalidad con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, modalidad)
            modalidad.delete()

            logger.info(f"El usuario '{request.user}' elimino la modalidad con id: {id}")
            return Response(
                {"message": f"La modalidad con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar la modalidad con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )