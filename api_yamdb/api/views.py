import uuid
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

from api.permissions import IsAdminUserOrReadOnly, IsModeratorPermission, \
    IsUserAdminModeratorOrReadOnly, IsModeratorPermission2
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleSerializer, UserSerializer,
                             ListTitleSerializer, TokenSerializer)
from rest_framework import filters, status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title, User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenViewSet(TokenObtainPairView):
    """Вьюсет для получения ТОКЕНА"""
    serializer_class = TokenSerializer


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Вьюсет для регистрации пользователя"""
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        username = serializer.initial_data.get('username')
        email = serializer.initial_data.get('email')
        if username == 'me':
            raise ValidationError('Запрещено имя "me", придумайте другое имя!')
        if not (username and email):
            serializer.is_valid(raise_exception=True)

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            if instance.email != email:
                raise ValidationError('У данного пользователя другая почта!')
            serializer.is_valid(raise_exception=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_unusable_password()
        instance.save()
        email = serializer.validated_data['email']

        code = uuid.uuid4()
        send_mail(
            'КОД ПОДТВЕРЖДЕНИЯ',
            f'Ваш код подтверждения!\n{code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        instance.confirmation_code = code
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


    # @action(detail=False, methods=['POST'])
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsModeratorPermission2],
        name='me'
    )
    def get_my_profile(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        if request.method == 'GET':
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data.get('role'):
                raise ValidationError('Нельзя менять самому себе роль!')
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    ordering = ('rating',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ListTitleSerializer
        return TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserAdminModeratorOrReadOnly,]
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

