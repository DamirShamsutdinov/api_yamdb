from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpViewSet, TitleViewSet, UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'^reviews/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(
    r'^reviews/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)
router.register('auth/signup', SignUpViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    # path(
    #     'auth/token/refresh/',
    #     TokenRefreshView.as_view(),
    #     name='token_refresh'
    # ),
]
