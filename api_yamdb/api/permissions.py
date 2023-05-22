from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """Доступ только пользователям с ролью 'User'"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsModerator(BasePermission):
    """Доступ только пользователям с ролью 'Moderator'"""
    def has_permission(self, request, view):
        return request.user and request.user.is_moderator


class IsAdmin(BasePermission):
    """Доступ только пользователям с ролью 'Admin'"""
    def has_permission(self, request, view):
        return request.user and request.user.is_admin
