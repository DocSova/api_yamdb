from django.contrib import admin
from django.db.models import Avg

from api_yamdb.constants import MAX_SEARCH_RESULTS, RATING_DEFAULT
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки раздела категорий."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_filter = ('name',)
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс настройки раздела жанров."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_filter = ('name',)
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    list_filter = ('name',)
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('name', 'year', 'category')

    @admin.display(description='Жанр/ы произведения')
    def get_genre(self, object):
        """Получает жанр или список жанров произведения."""
        return '\n'.join((genre.name for genre in object.genre.all()))

    # @admin.display(short_description='Количество отзывов',)
    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""

        return object.reviews.count()

    # @admin.display(short_description='Рейтинг',)
    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""

        rating = object.reviews.aggregate(average_score=Avg('score'))
        return round(rating.get('average_score'), RATING_DEFAULT)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Класс настройки соответствия жанров и произведений."""

    list_display = (
        'pk',
        'genre',
        'title'
    )
    list_filter = ('genre',)
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    list_filter = ('author', 'pub_date')
    list_per_page = MAX_SEARCH_RESULTS
    search_fields = ('author',)


admin.site.site_title = 'Администрирование YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
admin.site.empty_value_display = 'значение отсутствует'
