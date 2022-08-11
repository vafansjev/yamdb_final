from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin, ListModelMixin
                                   )
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from .filters import TitleFilter
from .permissions import (IsUserAdminModeratorOrReadOnly,
                          IsAuthenticatedAdminOrReadOnly,
                          )
from reviews.models import Category, Genre, Title, Review
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class CategoryViewSet(CreateModelMixin,
                      DestroyModelMixin, ListModelMixin,
                      viewsets.GenericViewSet
                      ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (IsAuthenticatedAdminOrReadOnly,)


class GenreViewSet(CreateModelMixin, DestroyModelMixin,
                   ListModelMixin, viewsets.GenericViewSet
                   ):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (IsAuthenticatedAdminOrReadOnly,)

    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticatedAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH",):
            return TitleCreateSerializer
        return TitleSerializer


@permission_classes([IsAuthenticatedOrReadOnly,
                    IsUserAdminModeratorOrReadOnly])
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("titles_id")
        review = get_object_or_404(Title, id=title_id)
        new_queryset = review.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("titles_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


@permission_classes([IsAuthenticatedOrReadOnly,
                    IsUserAdminModeratorOrReadOnly])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
