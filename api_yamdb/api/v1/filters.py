from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleGenreFilter(FilterSet):
    """Фильтр выборки произведений по определенным полям."""

    category = CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
