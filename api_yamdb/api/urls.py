from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet, \
    ReviewViewSet, CommentViewSet, UsersViewSet

router = DefaultRouter()
router.register("categories", CategoriesViewSet)
router.register("genres", GenresViewSet)
router.register("titles", TitlesViewSet)
router.register(r"^reviews/(?P<title_id>\d+)/reviews", ReviewViewSet)
router.register(
    r"^reviews/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet)
router.register("users", UsersViewSet)
router.register("users", UsersViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
         name="token_obtain_pair"
    ),
    path(
        "v1/auth/token/refresh/",
        TokenRefreshView.as_view(),
         name="token_refresh"
    ),
    path(
        "v1/auth/token/verify/",
        TokenVerifyView.as_view(),
         name="token_verify"),

]
