from rest_framework import serializers
from rest_framework.validators import ValidationError

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class SlugNameSerializer(serializers.ModelSerializer):
    """Сериализатор слагов."""

    class Meta:
        abstract = True
        fields = ('slug', 'name')


class CategorySerializer(SlugNameSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(SlugNameSerializer):
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
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

        def validate(self, data):
            """Запрещает пользователям оставлять повторные отзывы."""

            if not self.context.get('request').method == 'POST':
                return data
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
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

    role = serializers.StringRelatedField(read_only=True)
    username = serializers.SlugField(read_only=True)
    email = serializers.SlugField(read_only=True)

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


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор полей username и email
    для класса User с валидацией.
    """

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()
        if not any((user_by_username, user_by_email)):
            return User.objects.create(**validated_data)
        if user_by_username == user_by_email:
            return user_by_username
        response = {}
        if user_by_username:
            response['username'] = ['Уже занято']
        if user_by_email:
            response['email'] = ['Уже занято']
        raise ValidationError(response)


class GetTokenSerializer(serializers.Serializer):
    """
    Сериализатор полей username и confirmation_code
    для класса User с валидацией.
    """

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
