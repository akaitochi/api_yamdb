from rest_framework import serializers

from reviews.models import Categories, Genres, Titles, User
from reviews.validators import ValidateUsername, validate_year


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


# Верно ли разделить сериализаторы тайтлов на два?
class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов GET.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Titles
        read_only = True


class TitleWriteDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов POST, DELETE.
    """
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Titles


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
