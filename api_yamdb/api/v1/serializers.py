from rest_framework import serializers, validators

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
    class Meta(SlugNameSerializer.Meta):
        model = Category


class GenreSerializer(SlugNameSerializer):
    """Сериализатор жанров."""
    class Meta(SlugNameSerializer):

        class Meta(SlugNameSerializer):
            model = Genre


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор при get."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerFIeld(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений."""
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True,)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug',)

    class Meta:
        fields = '__all__'
        model = Title

    def display(self, instance):
        return TitleGETSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

        def validate(self, data):
            if not self.context['request'].method == 'POST':
                return data
            author = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise validators.ValidationError(
                    'Только 1 ревью на произведение!')
            return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        exclude = ('review')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для класса User с валидацией"""
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

    def validate(self, data):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError(
                {"username": ["This username is not awailable"]}
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор полей username и email
    для класса User с валидацией
    """
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError(
                {"username": ["This username is not awailable"]}
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    """
    Сериализатор полей username и confirmation_code
    для класса User с валидацией
    """
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
