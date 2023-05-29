from rest_framework import serializers

from reviews.models import User
from reviews.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя при регистрации"""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
        ])
    email = serializers.EmailField(required=True, max_length=254)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
        ])
    token = serializers.CharField(required=True)
