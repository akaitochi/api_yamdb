
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsSuperUserIsAdminIsModeratorIsAuthor)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteDeleteSerializer,
                          TokenSerializer, UserSerializer)

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


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    """Создает пользователя и отправляет код подтверждения."""

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDB registration',
        message=f'Your registration code {confirmation_code}',
        from_email=None,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    """"Создает JWT-токен для пользователей."""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if not default_token_generator.check_token(user, confirmation_code):
        raise serializers.ValidationError('Код подтверждения неверный!')
    message = {
        'Bearer': f'{AccessToken.for_user(user)}',
    }
    return Response(message, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Получение списка всех пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(methods=('get', 'patch',), detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


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
