from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from reviews.models import Categories, Genres, Titles
from .filters import TitleFilter
from .mixins import ModelMixinSet
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitleWriteDeleteSerializer
)


class CategoryViewSet(ModelMixinSet):
    """
    Получение списка всех категорий. Доступ без токена.
    """
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ''
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ModelMixinSet):
    """
    Получение списка всех жанров. Доступ без токена.
    """
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ''
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelMixinSet):
    """
    Получение списка всех произведений. Доступ без токена.
    """
    queryset = Titles.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = ''
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteDeleteSerializer
