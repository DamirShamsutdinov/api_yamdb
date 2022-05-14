from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Genre, Category, Title, Review, Comment

class UserSerializer(serializers.ModelSerializer):
    pass

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Genre

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Category

class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ListTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = fields

class ReviewSerializer(serializers.ModelSerializer):
    pass

class CommentSerializer(serializers.ModelSerializer):
    pass