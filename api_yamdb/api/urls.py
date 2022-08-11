from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)


v1_router = SimpleRouter()
v1_router.register(r"categories", CategoryViewSet, basename="categories")
v1_router.register(r"genres", GenreViewSet, basename="genres")
v1_router.register(r"titles", TitleViewSet, basename="titles")
v1_router.register(
    r"titles/(?P<titles_id>[^/.]+)/reviews", ReviewViewSet, basename="reviews"
)
v1_router.register(
    r"titles/(?P<titles_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include(v1_router.urls)),
]
