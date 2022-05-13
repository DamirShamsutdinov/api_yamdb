from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from api.views import CategoryViewSet, CommentViewSet, GenreViewSet, \
    ReviewViewSet, TitleViewSet, UsersViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'auth/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'),
]
