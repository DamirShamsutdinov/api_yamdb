from requests import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.permissions import IsModeratorPermission
from api.serializers import CategoriesSerializer, GenresSerializer, \
    TitlesSerializer, ReviewsSerializer, СommentsSerializer, UsersSerializer

from reviews.models import Category, Genre, Title, Review, Comment, User

from rest_framework import viewsets

from rest_framework.decorators import action


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminUser, IsModeratorPermission, IsAuthenticated)


    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsModeratorPermission],
        name='me'
    )
    def get_my_profile(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = UsersSerializer(user)
            return Response(serializer.data)
        if request.method == "PATCH":
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                user.save()
                return Response(serializer.data)
            raise serializer.ValidationError("Данные неверны!")


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsModeratorPermission,)

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.is_admin:
            serializer.save(author=self.request.user)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminUser,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminUser,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsModeratorPermission,)

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
    permission_classes = (IsModeratorPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
