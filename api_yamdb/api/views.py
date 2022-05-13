from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ValidationError

from api.permissions import (
    IsUserAdminModeratorOrReadOnly
)
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsUserAdminModeratorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('id')
        title = get_object_or_404(Title, pk=title_id)
        title_queryset = title.reviews.all()
        return title_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('id')
        title = get_object_or_404(Title, pk=title_id)
        reviews = self.request.user.reviews
        if reviews.filter(title).exists:
            raise ValidationError(
                msg='Вы уже оставляли обзор на данное произведение',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(author=self.request.user, title=title)
        avg_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = avg_rating['score__avg']
        title.save(update_fields=['rating'])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsUserAdminModeratorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('id')
        review = get_object_or_404(Review, pk=review_id)
        review_queryset = review.comments.all()
        return review_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
