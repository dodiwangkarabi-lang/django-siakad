from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("submit-krs/", views.submit_krs, name="submit_krs"),
    path("krs/", views.krs, name="krs"),
    path("kelas/", views.kelas, name="kelas"),
    path("gabung-kelas/", views.gabung_kelas, name="gabung_kelas"),
    path("", views.index, name="index"),
]