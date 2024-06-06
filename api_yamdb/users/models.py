from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.constants import (
    LENGTH_TEXT,
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH
)
from users.enums import UserRoles
from users.validators import validate_username_not_me


class User(AbstractUser):
    """Класс пользователей."""

    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Имя пользователя содержит недопустимый символ'
            ),
            validate_username_not_me,
        ],
    )
    email = models.EmailField(
        'E-mail',
        max_length=EMAIL_MAX_LENGTH,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=UserRoles.longest_role(),
        choices=UserRoles.choices(),
        default=UserRoles.user.name
    )
    confirmation_code = models.SlugField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:LENGTH_TEXT]

    @property
    def is_admin(self):
        return self.role == UserRoles.admin.name or self.is_staff

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name
