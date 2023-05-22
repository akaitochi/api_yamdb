from rest_framework import mixins, viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    pass


class ModeratorViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    pass


class AdminViewSet(viewsets.ModelViewSet):
    pass
