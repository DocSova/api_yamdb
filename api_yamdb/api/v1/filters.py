from django_filters.rest_framework import CharFilter, FilterSet
from reviews.models import Title


class TitleGenreFilter(FilterSet):
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug")

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']