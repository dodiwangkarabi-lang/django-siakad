from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("submit-krs/", views.submit_krs, name="submit_krs"),
    path("krs/", views.krs, name="krs"),
    path("kelas/", views.kelas, name="kelas"),
    path("kelola-krs/", views.kelola_krs, name="kelola_krs"),
    path("kelola-jadwal/", views.kelola_jadwal, name="kelola_jadwal"),
    path("gabung-kelas/", views.gabung_kelas, name="gabung_kelas"),
    path("", views.index, name="index"),
]