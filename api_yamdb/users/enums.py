from enum import Enum


class UserRoles(Enum):
    """Перечисление пользовательских ролей."""

    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    @classmethod
    def choices(cls):
        """Формирует соответствие констант и значений."""
        return tuple((attribute.name, attribute.value) for attribute in cls)

    @classmethod
    def longest_role(cls):
        """Возвращает самое длинное значение роли."""
        return len(max((role.value for role in cls), key=len))
