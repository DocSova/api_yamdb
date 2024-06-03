from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.filters import TitleGenreFilter
from api.v1.mixins import ListCreateDestroyViewSet
from api.v1.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsStaffOrAuthorOrReadOnly
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleGETSerializer,
    TitleSerializer,
    UserSerializer
)
from api.v1.utils import get_and_send_confirmation_code
from reviews.models import Category, Genre, Review, Title
from users.models import User


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

        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""

        return self.get_title().reviews.all()


class CategoryViewSet(ListCreateDestroyViewSet, viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet, viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    ordering_fields = ('name',)
    ordering = ('username',)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleGenreFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""

        if self.request.method in SAFE_METHODS:
            return TitleGETSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

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
    user = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    )
    if user.exists():
        get_and_send_confirmation_code(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.filter(
        username=serializer.data.get('username'),
        email=serializer.data.get('email')
    )
    get_and_send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
