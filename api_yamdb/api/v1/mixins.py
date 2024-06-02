from rest_framework import filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    max_search_results = 10
