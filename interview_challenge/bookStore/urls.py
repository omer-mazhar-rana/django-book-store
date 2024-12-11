from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserLoginView, UserRegisterView, UserLogoutView, BookViewSet


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
]
