from . import views

from django.urls import path

app_name = "auth_api"

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("me/", views.MeAPIView.as_view(), name="me"),
    path("get-role/", views.GetRoleAPIView.as_view(), name="get-role"),
]