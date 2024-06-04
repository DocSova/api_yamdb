from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'pk', 'username', 'email',
        'first_name', 'last_name',
        'bio', 'role')
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    list_editable = ('name', 'year', 'category')
    list_filter = ('year', 'genre', 'category')
    search_fields = ('name', 'description')

    def get_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genre.short_description = 'Жанры'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_editable = ('title', 'genre')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'pub_date', 'title')
    list_editable = ('text', 'author', 'score', 'title')
    list_filter = ('pub_date', 'score')
    search_fields = ('text', 'author__username')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    list_editable = ('text', 'author', 'review')
    list_filter = ('pub_date',)
    search_fields = ('text', 'author__username')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
