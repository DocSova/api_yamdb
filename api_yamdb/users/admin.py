from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from api_yamdb.constants import MAX_SEARCH_RESULTS

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Класс настройки раздела пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('username', 'role')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('bio', 'role',)}),
    )
