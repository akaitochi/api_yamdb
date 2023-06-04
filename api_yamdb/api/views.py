from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (IsAdminOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteDeleteSerializer)

DELETE_CONTENT = 'Удаление чужого контента запрещено!'


class CategoryViewSet(ModelMixinSet):
    """Получение списка всех категорий. Доступ без токена."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ModelMixinSet):
    """Получение списка всех жанров. Доступ без токена."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Получение списка всех произведений. Доступ без токена."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')
    serializer_class = TitleWriteDeleteSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteDeleteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение списка всех Отзывов. Доступ без токена."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Получение списка всех Комментариев. Доступ без токена."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
