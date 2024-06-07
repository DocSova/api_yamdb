from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models

from api_yamdb.constants import (
    CATEGORY_GENRE_NAME_LENGTH,
    LENGTH_TEXT,
    RATING_MAX,
    RATING_MIN,
    TITLE_NAME_LENGTH
)
from reviews.validators import validate_title_year


User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    """Родительский класс моделей Категории и Жанр."""

    name = models.CharField(
        'Hазвание',
        max_length=CATEGORY_GENRE_NAME_LENGTH,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='slug',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        abstract = True

        def __str__(self):
            return self.name[:LENGTH_TEXT]


class ReviewCommenBaseModel(models.Model):
    """Родительский класс моделей Отзыв и Комментарий."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Aвтор'
    )
    text = models.TextField(
        'Текст'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        abstract = True

        def __str__(self):
            return self.name[:LENGTH_TEXT]


class Category(CategoryGenreBaseModel):
    """Класс категорий."""

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBaseModel):
    """Класс жанров."""

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        'Hазвание',
        max_length=TITLE_NAME_LENGTH,
        db_index=True
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=[
            validate_title_year
        ],
        db_index=True
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class GenreTitle(models.Model):
    """Вспомогательный класс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'
        ordering = ('genre',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'


class Review(ReviewCommenBaseModel):
    """Класс отзывов."""

    score = models.PositiveSmallIntegerField(
        'Oценка',
        validators=[
            MinValueValidator(
                RATING_MIN,
                message=f'Введенная оценка ниже {RATING_MIN}'
            ),
            MaxValueValidator(
                RATING_MAX,
                message=f'Введенная оценка выше {RATING_MAX}'
            ),
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )

    class Meta(ReviewCommenBaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )
        default_related_name = 'reviews'


class Comment(ReviewCommenBaseModel):
    """Класс комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta(ReviewCommenBaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
