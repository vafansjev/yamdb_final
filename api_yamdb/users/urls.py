from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, get_token, signup_user


user_router = SimpleRouter()
user_router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(user_router.urls)),
    path("v1/auth/signup/", signup_user),
    path("v1/auth/token/", get_token),
]
