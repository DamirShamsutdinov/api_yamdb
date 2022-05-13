from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from reviews.models import Title, Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def ReviewValidation(self):
        title_id = self.kwargs.get('id')
        title = get_object_or_404(Title, pk=title_id)
        reviews = self.request.user.reviews
        if reviews.filter(title).exists:
            raise serializers.ValidationError(
                msg='Вы уже оставляли обзор на данное произведение',
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
