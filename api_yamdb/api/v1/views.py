
from rest_framework import mixins, viewsets


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Category."""
    pass


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Genre."""
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""
    pass


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Вьюсет для обьектов модели User."""
    pass
