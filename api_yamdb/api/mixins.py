from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.viewsets import GenericViewSet

from .permissions import (IsAdminOrReadOnly)


class ModelMixinSet(CreateModelMixin, DestroyModelMixin,
                    GenericViewSet, ListModelMixin):
    """Позволяет делать GET, POST, DELETE запросы."""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
