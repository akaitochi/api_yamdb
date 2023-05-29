from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
