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
    class Meta:
        fields = "__all__"
        model = Title

class ReviewSerializer(serializers.ModelSerializer):
    pass

class CommentSerializer(serializers.ModelSerializer):
    pass