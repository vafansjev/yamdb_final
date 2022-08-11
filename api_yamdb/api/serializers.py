import datetime
from rest_framework import serializers
from django.db.models import Avg
from django.db.models import IntegerField
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, title):
        reviews = Review.objects.filter(title=title)
        if reviews.exists():
            rating = reviews.aggregate(
                Avg('score', output_field=IntegerField()))['score__avg']
        else:
            rating = None
        return rating


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    description = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = datetime.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год не может быть больше текущего'
            )
        return value

    def validate_genre(self, value):
        genre = Genre.objects.filter(slug=value)
        if genre is None:
            raise serializers.ValidationError(
                'Данного жанра нет в списке'
            )
        return value

    def validate_category(self, value):
        category = Category.objects.all()
        if value not in category:
            raise serializers.ValidationError('Данной категории нет в списке')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['titles_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Повторно оставлять ревью нельзя')
        return data
