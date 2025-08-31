from typing import cast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from user_app.api.serializers import RegistrationSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def registration_view(request):
    """
    Register a new user, return token + basic info.
    """
    serializer = RegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        # Invalid input -> 400 with serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # serializer.save() returns a User instance (cast for type checker)
    account: User = cast(User, serializer.save())

    # Ensure a token exists for this user
    token, _ = Token.objects.get_or_create(user=account)

    data = {
        "response": "Registration Successful!",
        "username": account.username,
        "email": account.email,
        "token": token.key,
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login with username + password and return a token.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            "response": "Login successful.",
            "username": user.username,
            "email": user.email,
            "token": token.key,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout by deleting the current token. Idempotent/safe.
    """
    # TokenAuthentication sets request.auth = token instance
    token = getattr(request, "auth", None)
    if token:
        token.delete()
        return Response({"detail": "Logged out."}, status=status.HTTP_200_OK)

    # Fallback: delete any token linked to this user if present
    tok = Token.objects.filter(user=request.user).first()
    if tok:
        tok.delete()
        return Response({"detail": "Logged out."}, status=status.HTTP_200_OK)

    # Nothing to delete, treat as success
    return Response({"detail": "Already logged out."}, status=status.HTTP_200_OK)
