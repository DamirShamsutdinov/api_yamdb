from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment, User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review


class СommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
