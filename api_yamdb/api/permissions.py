from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsUser(permissions.BasePermission):
    """Доступ только пользователям с ролью 'User'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsModerator(permissions.BasePermission):
    """Доступ только пользователям с ролью 'Moderator'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    """Доступ только пользователям с ролью 'Admin'."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ только пользователея с ролью 'Admin', либо только чтение."""

    def has_permission(self, request, view):
        return request.method == 'GET' or (request.user.is_authenticated
                                           and (request.user.is_admin
                                                or request.user.is_superuser))


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю Джанго, админу Джанго, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author)
        )
