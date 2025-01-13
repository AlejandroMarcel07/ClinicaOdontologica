#IMPORTACIONES 1
from django.db import DatabaseError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
import logging

from yaml import serialize

# Configura el logger
logger = logging.getLogger(__name__)

#IMPORTACIONES 2
from .serializer import EstadoCitaSerializer
from .models import EstadoCitaModel
from ...Seguridad.permissions import CustomPermission


class EstadoCitaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadoCitaModel

    @swagger_auto_schema(
        responses={200: EstadoCitaSerializer(many=True)}
    )
    def get(self, request):
        try:
            estados = EstadoCitaModel.objects.all()
            estado_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            if estado_id and not estado_id.isdigit():
                raise ValidationError({"id": "El parametro 'id' debe de ser un numero"})
            if estado_id:
                estados = estados.filter(id=estado_id)
            if nombre:
                estados = estados.filter(nombre__icontains=nombre)

            serializer = EstadoCitaSerializer(estados, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {estados.count()} estados de cita.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los estados cita: {e}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=EstadoCitaSerializer, responses={201: EstadoCitaSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = EstadoCitaSerializer(data=data)
            if serializer.is_valid():
                estadoCita = serializer.save()
                logger.info(f"El usuario '{request.user}' creó un nuevo estado de cita con id: '{estadoCita.id}'")
                return Response(
                    {"message": "Estado de cita creado exitosamente.", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Errores de validación en la solicitud de {request.user}: {serializer.errors}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error interno del servidor: {str(e)}")
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=EstadoCitaSerializer, responses={200: EstadoCitaSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                estadoCita = EstadoCitaModel.objects.get(id=id)
            except EstadoCitaModel.DoesNotExist:
                logger.warning(f"El Estado cita con id {id} no existe.")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado de cita con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = EstadoCitaSerializer(estadoCita, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.data}' actualizo el Estado de cita con id {id}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error interno del servidor al actualizar el Estado de cita con id {id}: {str(e)}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                estadoCita = EstadoCitaModel.objects.get(id=id)
            except EstadoCitaModel.DoesNotExist:
                logger.warning(f"El Estado de cita con id {id} no existe.")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado de cita con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            #Permiso de objeto
            self.check_object_permissions(request, estadoCita)
            estadoCita.delete()

            logger.info(f"El usuario '{request.user}' elimino el Estado de cita con id: {id}")
            return  Response(
                {"message": f"El Estado de cita con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el genero con id {id}: {str(e)}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



