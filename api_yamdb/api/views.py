from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from reviews.models import Categories, Genres, Titles, Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

DELETE_CONTENT = 'Удаление чужого контента запрещено!'


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


class ReviewViewSet(ModelViewSet):
    """
    Получение списка всех Отзывов. Доступ без токена.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(
            title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceprion=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(ModelViewSet):
    """
    Получение списка всех Комментариев. Доступ без токена.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied(DELETE_CONTENT)
        super().perform_destroy(serializer)