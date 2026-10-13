from django.urls import path

from . import views

app_name = "accounts_web"

urlpatterns = [
    path("login/", views.login_view, name="login"),
]