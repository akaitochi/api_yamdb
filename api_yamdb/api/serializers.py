from rest_framework import serializers

from reviews.models import User
from reviews.validators import ValidateUsername


class UserSerializer(ValidateUsername, serializers.ModelSerializer):
    """Сериализация данных пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(ValidateUsername, serializers.Serializer):
    """Сериализация данных пользователя при регистрации"""
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(required=True, max_length=254)


class TokenSerializer(ValidateUsername, serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    token = serializers.CharField(required=True)
