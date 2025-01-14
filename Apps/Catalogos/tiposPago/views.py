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
from .serializer import TipoPagoSerializer
from .models import TipoPagoModel
from ...Seguridad.permissions import CustomPermission

class TipoPagoApiView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoPagoModel

    @swagger_auto_schema(
        responses={200: TipoPagoSerializer(many=True)}
    )
    def get(self, request):
        try:
            tipopago = TipoPagoModel.objects.all()

            #Verificar que haigan parametros para filtrar
            tipopago_id = request.query_params.get('id', None)
            nombre = request.query_params.get('nombre', None)

            #Validar
            if tipopago_id and not tipopago_id.isdigit():
                raise  ValidationError({"error": "El parametro 'id' debe de ser un numero"})

            #Filtrar por parametros
            if tipopago_id:
                tipopago = tipopago.filter(id=tipopago_id)
            if nombre:
                tipopago = tipopago.filter(nombre__icontains=nombre)

            serializer = TipoPagoSerializer(tipopago, many=True)
            logger.info(f"El usuario '{request.user}' recuperó {tipopago.count()} tipo de pago.")
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except DatabaseError as e:
            logger.error(f"Error al recuperar los tipo de pagos: {e}, usuario: {request.user}")
            return Response ({"error": "Hubo un problema al recuperar los datos."},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        request_body=TipoPagoSerializer, responses={201: TipoPagoSerializer}
    )
    def post(self, request):
        try:
            data = request.data
            serializer = TipoPagoSerializer(data=data)

            if serializer.is_valid():
                tipopago = serializer.save()
                logger.info(
                    f"El usuario '{request.user}' creó un nuevo tipo de pago con id: '{tipopago.id}'"
                )
                return Response(
                    {
                        "message": "Tipo de pago creado exitosamente.",
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
        request_body=TipoPagoSerializer, responses={200: TipoPagoSerializer}
    )
    def patch(self, request, id=None):
        try:
            try:
                tipopago = TipoPagoModel.objects.get(id=id)
            except TipoPagoModel.DoesNotExist:
                logger.warning(f"El Tipo pago con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Tipo pago con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = TipoPagoSerializer(tipopago, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"El usuario '{request.user}' actualizo el Tipo de pago con id {id}")
                return Response(
                    {
                        "message": "Tipo de pago actualizado exitosamente.",
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
            logger.error(f"Error interno del servidor al actualizar el Tipo de pago con id {id}: {str(e)}, usuario: {request.user}")
            return  Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo mas tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, id=None):
        try:
            try:
                tipopago = TipoPagoModel.objects.get(id=id)
            except TipoPagoModel.DoesNotExist:
                logger.warning(f"El Tipo de pago con id {id} no existe, usuario: {request.user}")
                return  Response(
                    {"error": {
                        'Id':{
                            f"El Tipo de pago con id {id} no existe."
                        }
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )

            self.check_object_permissions(request, tipopago)
            tipopago.delete()

            logger.info(f"El usuario '{request.user}' elimino el Tipo de pago con id: {id}")
            return Response(
                {"message": f"El Tipo de pago con Id {id} eliminado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error interno del servidor al intentar eliminar el Tipo de pago con id {id}: {str(e)}, usuario: {request.user}"),
            return Response(
                {"error": "Error interno del servidor. Por favor intentelo de nuevo más tarde."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
