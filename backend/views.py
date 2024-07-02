from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

# auth settings
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password  # hashear password
from rest_framework.authtoken.models import Token

# auth and permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated  # authentication
from rest_framework.authentication import TokenAuthentication  # permissions


from .serializer import UserSerializer

# redis
from django.views.decorators.cache import cache_page



@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Crear token
    token = Token.objects.get_or_create(user=user)

    # intance to serialize
    serializer = UserSerializer(instance=user)

    return Response(
        {"token": token[0].key, "user": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def register(request):
    data = request.data
    serializer = UserSerializer(
        data={**data, "password": make_password(data["password"])}
    )

    if serializer.is_valid():
        serializer.save()

        token = Token.objects.create(user=serializer.instance)
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": serializer.instance.id,
                    "username": serializer.instance.username,
                    "email": serializer.instance.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes(
    [TokenAuthentication]
)  # Requiere Header Authorization con 'Token <token>' - method to authenticate
@permission_classes([IsAuthenticated])  # Authentication
@cache_page(60 * 15)  # cache for 15 minutes
def profile(request):
    auth_user = request.user

    return Response(
        {
            "message": "User profile",
            "user": {
                "id": auth_user.id,
                "username": auth_user.username,
                "email": auth_user.email,
            },
        },
        status=status.HTTP_200_OK,
    )
