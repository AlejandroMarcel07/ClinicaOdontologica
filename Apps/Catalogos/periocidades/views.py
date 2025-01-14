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
from .serializer import PeriocidadSerializer
from .models import PeriocidadModel
from ...Seguridad.permissions import CustomPermission

class PeriocidadApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = PeriocidadModel

    @swagger_auto_schema(
        responses={200: PeriocidadSerializer(many=True)}
    )
    def get(self, request):
        try:
            periocidades = PeriocidadModel.objects.all()

            #Verificar que haigan parametros para filtrar
            periocidad_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if periocidad_id and not periocidad_id.isdigit():
                raise  ValidationError({"id": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if periocidad_id:
                periocidades = periocidades.filter(id=periocidad_id)
            if nombre:
                periocidades = periocidades.filter(nombre__icontains=nombre)

            serializer = PeriocidadSerializer(periocidades, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {periocidades.count()} periocidades.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar las periocidades: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @swagger_auto_schema(
        request_body=PeriocidadSerializer, responses={201: PeriocidadSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = PeriocidadSerializer(data=data)

            if serializer.is_valid():
                periodo = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo periodo con id: '{periodo.id}'"
                )
                return Response(
                    {
                        "message": "Periodo creado exitosamente.",
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
        request_body=PeriocidadSerializer, responses={200: PeriocidadSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                periodo = PeriocidadModel.objects.get(id=id)
            except PeriocidadModel.DoesNotExist:
                logger.warning(f"El Periodo con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Periodo con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = PeriocidadSerializer(periodo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo el Periodo con id {id}")
                return Response(
                    {
                        "message": "Periodo actualizado exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar el Periodo con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                periodo = PeriocidadModel.objects.get(id=id)
            except PeriocidadModel.DoesNotExist:
                logger.warning(f"El Periodo con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Periodo con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, periodo)
            periodo.delete()

            logger.info(f"El usuario '{request.user}' elimino el Periodo con id: {id}")
            return Response(
                {"message": f"El Periodo con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el Tratamiento con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
