#IMPORTACIONES 1
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status

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
        generos = GeneroModel.objects.all()
        serializer = GeneroSerializer(generos, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
