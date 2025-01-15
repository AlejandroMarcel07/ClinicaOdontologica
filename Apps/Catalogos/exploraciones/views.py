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
from .serializer import ExploracionSerializer
from .models import ExploracionModel
from ...Seguridad.permissions import CustomPermission

class ExploracionApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = ExploracionModel

    @swagger_auto_schema(
        responses={200: ExploracionSerializer(many=True)}
    )
    def get(self, request):
        try:
            exploraciones = ExploracionModel.objects.all()

            #Verificar que haigan parametros para filtrar
            exploracion_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if exploracion_id and not exploracion_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if exploracion_id:
                exploraciones = exploraciones.filter(id=exploracion_id)
            if nombre:
                exploraciones = exploraciones.filter(nombre__icontains=nombre)

            serializer = ExploracionSerializer(exploraciones, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {exploraciones.count()} exploraciónes.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar las exploraciónes: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=ExploracionSerializer, responses={201: ExploracionSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = ExploracionSerializer(data=data)

            if serializer.is_valid():
                exploracion = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó una nueva exploración con id: '{exploracion.id}'"
                )
                return Response(
                    {
                        "message": "Exploración creada exitosamente.",
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
        request_body=ExploracionSerializer, responses={200: ExploracionSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                exploracion = ExploracionModel.objects.get(id=id)
            except ExploracionModel.DoesNotExist:
                logger.warning(f"La Exploración con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"La Exploración con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ExploracionSerializer(exploracion, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo la exploración con id {id}")
                return Response(
                    {
                        "message": "Exploración actualizada exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar la exploración con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                exploracion = ExploracionModel.objects.get(id=id)
            except ExploracionModel.DoesNotExist:
                logger.warning(f"La Exploración con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"La Exploración con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, exploracion)
            exploracion.delete()

            logger.info(f"El usuario '{request.user}' elimino la exploración con id: {id}")
            return Response(
                {"message": f"La Exploración con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar la exploración con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )