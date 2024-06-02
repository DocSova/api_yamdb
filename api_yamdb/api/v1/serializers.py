import re
from rest_framework import serializers
from rest_framework.validators import ValidationError

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

    def display(self, instance):
        return TitleGETSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('title',)
        model = Review

        def validate(self, data):
            """Запрещает пользователям оставлять повторные отзывы."""

            request = self.context.get('request')
            if request.method == 'POST':
                title_id = self.context.get('view').kwargs.get('title_id')
                title = get_object_or_404(Title, pk=title_id)
                if title.reviews.filter(author=request.user).exists():
                    raise serializers.ValidationError(
                        'Вы уже оставили отзыв на данное произведение!'
                    )
            return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для класса User с валидацией."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)

    class Meta:
        model = User
        ordering = ['id']
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError(
                {'email': ['Неверные учетные данные.']}
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ['Пользователь с таким email уже существует.']}
            )
        return email

    def validate_username(self, username):
        if not username:
            raise serializers.ValidationError(
                {'username': ['Неверные учетные данные.']}
            )
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                {'username': ['Недопустимое значение']}
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ['Пользователь с таким username уже существует.']}
            )
        return username


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор полей username и email
    для класса User с валидацией.
    """

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user


class GetTokenSerializer(serializers.Serializer):
    """
    Сериализатор полей username и confirmation_code
    для класса User с валидацией.
    """

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
