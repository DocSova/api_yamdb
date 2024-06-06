from django.core.exceptions import ValidationError

from api_yamdb.constants import RESTRICTED_USERNAMES


def validate_username_not_me(value):
    """Валидация на запрещенные никнеймы."""
    if value in RESTRICTED_USERNAMES:
        msg = f'Имя пользователя "{value}" использовать нельзя'
        raise ValidationError(msg)
