import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )
    description = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Введен год из будущего'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all(),
        required=False
    )
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Выберите оценку от 1 до 10')
        return value

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                    title=title, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    "Можно оставить только 1 отзыв на произведение.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Review.objects.all(),
        required=False
    )

    class Meta:
        fields = '__all__'
        model = Comment
