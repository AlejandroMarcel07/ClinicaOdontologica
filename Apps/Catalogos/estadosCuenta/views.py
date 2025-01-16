#IMPORTACIONES 1
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
from .serializer import EstadoCuentaSerializer
from .models import EstadoCuentaModel
from ...Seguridad.permissions import CustomPermission

class EstadoCuentaApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadoCuentaModel

    @swagger_auto_schema(
        responses={200: EstadoCuentaSerializer(many=True)}
    )
    def get(self, request):
        try:
            estados = EstadoCuentaModel.objects.all()

            # Verificar que haigan parametros para filtrar
            estados_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            # Validar
            if estados_id and not estados_id.isdigit():
                raise ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            # Filtrar por parametros
            if estados_id:
                estados = estados.filter(id=estados_id)
            if nombre:
                estados = estados.filter(nombre__icontains=nombre)

            serializer = EstadoCuentaSerializer(estados, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {estados.count()} estados de cuenta.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los estados de cuenta: {e}, usuario: {request.user}")
            return Response({"error": "Hubo un problema al recuperar los datos."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=EstadoCuentaSerializer, responses={201: EstadoCuentaSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = EstadoCuentaSerializer(data=data)

            if serializer.is_valid():
                estado = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo Estado de cuenta con id: '{estado.id}'"
                )
                return Response(
                    {
                        "message": "Estado cuenta creado exitosamente.",
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
        request_body=EstadoCuentaSerializer, responses={200: EstadoCuentaSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                estado = EstadoCuentaModel.objects.get(id=id)
            except EstadoCuentaModel.DoesNotExist:
                logger.warning(f"El Estado de cuenta con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado cuenta con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = EstadoCuentaSerializer(estado, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo el Estado de cuenta con id {id}")
                return Response(
                    {
                        "message": "Estado cuenta actualizado exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar el Estao de cuenta con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                estado = EstadoCuentaModel.objects.get(id=id)
            except EstadoCuentaModel.DoesNotExist:
                logger.warning(f"El Estado de cuenta con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Estado cuenta con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, estado)
            estado.delete()

            logger.info(f"El usuario '{request.user}' elimino el Estado de cuenta con id: {id}")
            return Response(
                {"message": f"El Estado de cuenta con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el Estado de cuenta con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


