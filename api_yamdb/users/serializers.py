from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate(self, attrs):
        if len(attrs["username"]) <= 3:
            raise serializers.ValidationError(
                "Имя пользователя должно быть больше трех символов!"
            )
        if attrs["username"] == attrs["email"]:
            raise serializers.ValidationError(
                "Поля email и username не должны совпадать."
            )
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует!"
            )
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует!"
            )
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs["username"])
        confirmation_code = attrs["confirmation_code"]
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError("Неверный код подтверждения!")
        return attrs
