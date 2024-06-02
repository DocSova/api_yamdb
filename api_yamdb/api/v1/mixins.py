from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAdminOrReadOnly


class SlugNameViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name')
    max_search_results = 10
