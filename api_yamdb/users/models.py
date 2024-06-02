from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import LENGTH_TEXT

from .enums import UserRoles
from .validators import validate_username_not_me


class User(AbstractUser):
    """Класс пользователей."""

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ'
            ),
            validate_username_not_me,
        ],
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=UserRoles.choices(),
        default=UserRoles.user.name
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:LENGTH_TEXT]

    @property
    def is_admin(self):
        return self.role == UserRoles.admin.name

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name

    @property
    def is_user(self):
        return self.role == UserRoles.user.name
