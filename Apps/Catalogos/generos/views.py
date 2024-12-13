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
from .serializer import GeneroSerializer
from .models import GeneroModel
from ...Seguridad.permissions import CustomPermission


class GeneroApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = GeneroModel

    @swagger_auto_schema(
        responses={200: GeneroSerializer(many=True)}
    )
    def get(self, request):
        try:
            generos = GeneroModel.objects.all()

            #Verificar que haigan parametros para filtrar
            genero_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if genero_id and not genero_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if genero_id:
                generos = generos.filter(id=genero_id)
            if nombre:
                generos = generos.filter(nombre__icontains=nombre)

            serializer = GeneroSerializer(generos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {generos.count()} generos.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los generos: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        request_body=GeneroSerializer, responses={201: GeneroSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = GeneroSerializer(data=data)
            if serializer.is_valid():
                genero = serializer.save()
                logger.info(f"El usuario '{request.user}' creo un nuevo genero con id: '{genero.id}'")
                return Response(
                    {"message": "Genero creado exitosamente.", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Errores de validacion: {serializer.errors}")
                return  Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error interno del servidor: {str(e)}")
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @swagger_auto_schema(
        request_body=GeneroSerializer, responses={200: GeneroSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                genero = GeneroModel.objects.get(id=id)
            except GeneroModel.DoesNotExist:
                logger.warning(f"El genero con id {id} no existe.")
                return Response(
                    {"error": f"El genero con id {id} no existe."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = GeneroSerializer(genero, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizó el genero con id: {id}")
                return Response(
                    {"message": "Genero actualizado exitosamente.", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                logger.warning(f"Errores de validación al actualizar el genero con id {id}: {serializer.errors}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error interno del servidor al actualizar el genero con id {id}: {str(e)}")
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                genero = GeneroModel.objects.get(id=id)
            except GeneroModel.DoesNotExist:
                logger.warning(f"El genero con id {id} no existe.")
                return Response(
                    {"error": f"El genero con id {id} no existe."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verificar permisos por objeto, si es necesario
            self.check_object_permissions(request, genero)

            genero.delete()
            logger.info(f"El usuario '{request.user}' eliminó el genero con id: {id}")
            return Response(
                {"message": f"Genero con id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el genero con id {id}: {str(e)}")
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
