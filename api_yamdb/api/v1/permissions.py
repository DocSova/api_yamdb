from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Предоставляет право на запросы только
    админу и суперюзеру.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Ограничивает анонима правом на безопасные запросы.
    Аутентифицированному пользователю предоставляет право
    на запросы POST. Все типы запросов доступны только
    админу, модератору и суперюзеру. 
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_authenticated

        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )


class ReadOnly(permissions.BasePermission):
    """Ограничивает анонима правом на безопасные запросы."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
