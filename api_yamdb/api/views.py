from rest_framework.viewsets import ModelViewSet

from reviews.models import Categories, Genres, Titles


class CategoryViewSet(ModelViewSet):
    """
    Получение списка всех категорий. Доступ без токена.
    """
    queryset = Categories.objects.all()
    serializer_class = ''
    permission_classes = ''


class GenreViewSet(ModelViewSet):
    """
    Получение списка всех жанров. Доступ без токена.
    """
    queryset = Genres.objects.all()
    serializer_class = ''
    permission_classes = ''


class TitleViewSet(ModelViewSet):
    """
    Получение списка всех произведений. Доступ без токена.
    """
    queryset = Titles.objects.all()
    serializer_class = ''
    permission_classes = ''
