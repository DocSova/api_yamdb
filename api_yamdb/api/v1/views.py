from rest_framework import mixins, status, viewsets, filters, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleGenreFilter
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGETSerializer,
    TitleSerializer,
    UserSerializer,
    GetTokenSerializer,
    SignUpSerializer
)
from .permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    IsAuthorModeratorAdminOrReadOnly,
    IsStaffOrAuthorOrReadOnly
)
from .utils import get_and_send_confirmation_code
from .mixins import ListCreateDestroyMixin


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        """Возвращает объект текущего отзыва."""

        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id'],
        )

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""

        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва,
        где автором является текущий пользователь."""

        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_title(self):
        """Возвращает объект текущего произведения."""
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения,
        где автором является текущий пользователь."""
        title = self.get_title()
        author = self.request.user

        """Проверяем, существует ли уже обзыв от этого пользователя"""
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError('Вы уже оставили обзор.')

        serializer.save(author=author, title=title)

    def get_queryset(self):
        """Возвращает queryset с отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""

        return self.get_title().reviews.all()


class CategoryViewSet(ListCreateDestroyMixin, viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyMixin, viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleGenreFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""

        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleGETSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """Вьюсет для обьектов модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=('get', 'patch', 'delete'),
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_selfpage(self, request, username):
        """Обеспечивает получание данных пользователя по его username и
        управление ими."""

        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_me_data(self, request):
        """Позволяет пользователю получить подробную информацию о себе
        и редактировать её."""

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data['username'])
    if serializer.data['confirmation_code'] == user.confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        'Проверьте правильность указанных для получения токена данных.',
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def signup(request):
    user = User.objects.filter(username=request.data.get('username'), email=request.data.get('email'))
    if user.exists():
        get_and_send_confirmation_code(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.filter(username=serializer.data.get('username'), email=serializer.data.get('email'))
        get_and_send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
