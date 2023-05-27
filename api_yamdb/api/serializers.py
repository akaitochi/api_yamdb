from rest_framework import serializers

from reviews.models import Categories, Genres, Titles
from reviews.validators import validate_year


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
    genre = GenreSerializer(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = CategorySerializer(
        queryset=Categories.objects.all(),
        slug_fields='slug'
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Titles
