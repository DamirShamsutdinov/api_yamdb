from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet, CommentViewSet, GenresViewSet, \
    ReviewViewSet, TitlesViewSet, UsersViewSet

router = DefaultRouter()
router.register("categories", CategoriesViewSet)
router.register("genres", GenresViewSet)
router.register('titles', TitlesViewSet)
router.register(r"^reviews/(?P<title_id>\d+)/reviews", ReviewViewSet)
router.register(
    r"^reviews/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet)
router.register("users", UsersViewSet)
router.register("users", UsersViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
