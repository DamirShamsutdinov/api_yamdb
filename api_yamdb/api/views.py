from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

class CategoriesViewSet(viewsets.ModelViewset):
    pass


class CommentViewSet(viewsets.ModelViewset):
    pass


class GenresViewSet(viewsets.ModelViewset):
    pass


class ReviewViewSet(viewsets.ModelViewset):
    pass


class TitlesViewSet(viewsets.ModelViewset):
    pass


class UsersViewSet(viewsets.ModelViewset):
    pass
