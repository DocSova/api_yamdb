from rest_framework import filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from api_yamdb.constants import MAX_SEARCH_RESULTS
from api.v1.permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    max_search_results = MAX_SEARCH_RESULTS
