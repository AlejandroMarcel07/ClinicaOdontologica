from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserCreateSerializer
from .models import User
from drf_yasg.utils import swagger_auto_schema

class UserCreateView(APIView):

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Crear el usuario
            return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: UserCreateSerializer(many=True)}
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserCreateSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)