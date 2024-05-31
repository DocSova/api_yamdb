
import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (GetTokenSerializer,
                          SignUpSerializer,)
from users.models import User
from api_yamdb.settings import EMAIL_YAMDB



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


def get_and_send_confirmation_code(user):
    user.update(confirmation_code=str(uuid.uuid4()).split("-")[0])
    send_mail(
        'Код подтверждения',
        (f'Код подтверждения для пользователя "{user[0].username}":'
         f' {user[0].confirmation_code}'),
        EMAIL_YAMDB,
        [user[0].email]
    )


@api_view(['POST'])
def signup(request):
    user = User.objects.filter(**request.data)
    if user.exists():
        get_and_send_confirmation_code(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.filter(**serializer.data)
        get_and_send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
