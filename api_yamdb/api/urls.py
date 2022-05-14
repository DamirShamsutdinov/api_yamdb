from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpViewSet, TitleViewSet, UserViewSet,
                       TokenViewSet,
                       )

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
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
router.register('auth/signup', SignUpViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenViewSet),
]
