from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from api.permissions import IsAdmin
from .models import User
from .serializers import (
    UserSerializer,
    SignupSerializer,
    TokenSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "username"

    @action(["GET", "PATCH"],
            detail=False,
            permission_classes=([IsAuthenticated]))
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        role = request.user.role
        serializer.save(role=role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_user(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data["username"]
    email = serializer.data["email"]
    user = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user[0])
    user[0].confirmation_code = confirmation_code
    user[0].save()
    send_mail(
        f"YamDb registration for {username}",
        f"Your confirmation_code: {confirmation_code}",
        "do-not-reply@yamdb.ru",
        [f"{email}"],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    print(f"{serializer}")
    serializer.is_valid(raise_exception=True)
    print("IS VALID")
    username = serializer.data["username"]
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({"token": str(token)}, status=status.HTTP_200_OK)
