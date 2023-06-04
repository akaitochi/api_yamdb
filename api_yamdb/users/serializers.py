from rest_framework import serializers

from reviews.validators import ValidateUsername
from .models import User


class UserSerializer(ValidateUsername, serializers.ModelSerializer):
    """Сериализация данных пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(ValidateUsername, serializers.Serializer):
    """Сериализация данных пользователя при регистрации."""

    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(required=True, max_length=254)


class TokenSerializer(ValidateUsername, serializers.Serializer):
    """Сериализация данных пользователя при получении токена."""
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(required=True)
