from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя при регистрации"""
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        """Проверяем, что нельзя использовать 'me' в качестве username"""
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(
                'Пользователя с username "me" нельзя создавать'
            )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        max_length=150,
        validators=[
            validate_username,
        ])
    token = serializers.CharField(required=True)
