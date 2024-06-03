from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly
)


class IsAdmin(BasePermission):
    """Предоставление прав админу и суперюзеру."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_staff
        )


class ReadOnly(BasePermission):
    """Ограничивает анонима правом на безопасные запросы."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Доступ разрешен только администратору."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsStaffOrAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Доступ разрешен только администратору, модератору или автору."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
            or request.user == obj.author
        )
