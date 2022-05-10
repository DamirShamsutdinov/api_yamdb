from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser

from api.permissions import IsAuthorModeratorOrReadOnlyPermission, \
    IsSuperuserPermission
from api.serializers import CategoriesSerializer, GenresSerializer, \
    TitlesSerializer, ReviewsSerializer, СommentsSerializer, UsersSerializer

from reviews.models import Category, Genre, Title, Review, Comment, User


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperuserPermission,)

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.is_admin:
            serializer.save(author=self.request.user)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperuserPermission,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperuserPermission,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorModeratorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("post_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = СommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorModeratorOrReadOnlyPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
