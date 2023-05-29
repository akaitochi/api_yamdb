from sqlite3 import IntegrityError
from rest_framework import pagination, serializers, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from users.models import User
from .permissions import IsAdmin
from .serializers import SignUpSerializer, UserSerializer


@api_view(['POST'])
def signup(request):
    """Создает пользователя и отправляет код подтверждения"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise serializers.ValidationError
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDB registration',
        message=f'Your registration code {confirmation_code}',
        from_email=None,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = pagination.PageNumberPagination

    @action(methods=('get', 'patch',), detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
