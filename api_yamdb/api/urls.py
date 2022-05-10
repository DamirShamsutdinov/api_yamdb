from django.db import router
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    GenreViewSet,
    CategoryViewSet,
    TitleViewSet,
    UsersViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router = DefaultRouter()
router.register("genres", GenreViewSet, basename='genres')
router.register("categories", CategoryViewSet, basename='categories')
router.register("titles", TitleViewSet, basename='titles')
router.register(
    r"^titles/(?P<title_id>\d+)/",
    TitleViewSet, basename="title"
)
router.register("users", UsersViewSet, basename='genres')


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/auth", include("djoser.urls")),
    path("v1/auth", include("djoser.urls.jwt")),
]
