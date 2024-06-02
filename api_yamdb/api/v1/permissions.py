from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


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


class ReadOnly(permissions.BasePermission):
    """Ограничивает анонима правом на безопасные запросы."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Доступ разрешен только администратору."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsStaffOrAuthorOrReadOnly(BasePermission):
    """Доступ разрешен только администратору, модератору или автору."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
            or request.user == obj.author
        )
