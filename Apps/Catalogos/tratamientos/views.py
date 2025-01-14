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
from .serializer import TratamientoSerializer
from .models import TratamientoModel
from ...Seguridad.permissions import CustomPermission

class TratamientoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TratamientoModel

    @swagger_auto_schema(
        responses={200: TratamientoSerializer(many=True)}
    )
    def get(self, request):
        try:
            tratamientos = TratamientoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            tratamiento_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if tratamiento_id and not tratamiento_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if tratamiento_id:
                tratamientos = tratamientos.filter(id=tratamiento_id)
            if nombre:
                tratamientos = tratamientos.filter(nombre__icontains=nombre)

            serializer = TratamientoSerializer(tratamientos, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {tratamientos.count()} tratamientos.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los tratamientos: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=TratamientoSerializer, responses={201: TratamientoSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = TratamientoSerializer(data=data)

            if serializer.is_valid():
                tratamiento = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo tratamiento con id: '{tratamiento.id}'"
                )
                return Response(
                    {
                        "message": "Tratamiento creado exitosamente.",
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
        request_body=TratamientoSerializer, responses={200: TratamientoSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                tratamiento = TratamientoModel.objects.get(id=id)
            except TratamientoModel.DoesNotExist:
                logger.warning(f"El Tratamiento con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Tratamiento con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = TratamientoSerializer(tratamiento, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo el Tratamiento con id {id}")
                return Response(
                    {
                        "message": "Tratamiento actualizado exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar el tratamiento con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                tratamiento = TratamientoModel.objects.get(id=id)
            except TratamientoModel.DoesNotExist:
                logger.warning(f"El Tratamiento con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Tratamiento con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, tratamiento)
            tratamiento.delete()

            logger.info(f"El usuario '{request.user}' elimino el Tratamiento con id: {id}")
            return Response(
                {"message": f"El Tratamiento con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el Tratamiento con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )