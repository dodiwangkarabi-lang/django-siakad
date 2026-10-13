from django.urls import path, include

from .web import views

app_name = "penugasan"

urlpatterns = [
    path("tugas/<int:penugasan_id>/", views.kirim_tugas, name="kirim_tugas"),
    path("tugas/", views.daftar_tugas, name="daftar_tugas"),
    path("kelas/<int:kelas_id>/tugas/", views.daftar_tugas_by_kelas, name="daftar_tugas_by_kelas"),
    path("penugasan/<int:penugasan_id>/pengumpulan/", views.detail_penugasan, name="detail_penugasan"),
]