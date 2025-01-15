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
from .serializer import FrecuenciaSerializer
from .models import FrecuenciaModel
from ...Seguridad.permissions import CustomPermission

class FrecuenciaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = FrecuenciaModel

    @swagger_auto_schema(
        responses={200: FrecuenciaSerializer(many=True)}
    )
    def get(self, request):
        try:
            frecuencias = FrecuenciaModel.objects.all()

            #Verificar que haigan parametros para filtrar
            frecuencia_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if frecuencia_id and not frecuencia_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if frecuencia_id:
                frecuencias = frecuencias.filter(id=frecuencia_id)
            if nombre:
                frecuencias = frecuencias.filter(nombre__icontains=nombre)

            serializer = FrecuenciaSerializer(frecuencias, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {frecuencias.count()} frecuencias.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar las frecuencias: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        request_body=FrecuenciaSerializer, responses={201: FrecuenciaSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = FrecuenciaSerializer(data=data)

            if serializer.is_valid():
                frecuencia = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nueva frecuencia con id: '{frecuencia.id}'"
                )
                return Response(
                    {
                        "message": "Frecuencia creada exitosamente.",
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
        request_body=FrecuenciaSerializer, responses={200: FrecuenciaSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                frecuencia = FrecuenciaModel.objects.get(id=id)
            except FrecuenciaModel.DoesNotExist:
                logger.warning(f"La Frecuencia con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"La Frecuencia con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = FrecuenciaSerializer(frecuencia, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo la frecuenica con id {id}")
                return Response(
                    {
                        "message": "Frecuencia actualizada exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar la frecuencia con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                frecuencia = FrecuenciaModel.objects.get(id=id)
            except FrecuenciaModel.DoesNotExist:
                logger.warning(f"La Frecuecia con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"La Frecuencia con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, frecuencia)
            frecuencia.delete()

            logger.info(f"El usuario '{request.user}' elimino la frecuencia con id: {id}")
            return Response(
                {"message": f"La frecuencia con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar la frecuencia con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
