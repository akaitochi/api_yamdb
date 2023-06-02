from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import ValidateUsername, validate_year


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов GET."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        many=True
    )
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'rating', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title
        read_only = True


class TitleWriteDeleteSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов POST, DELETE."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = (
            'id', 'rating', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


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


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Вы не можете добавить более одного отзыва на произведение'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
