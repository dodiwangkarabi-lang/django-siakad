
from django.urls import path

from academic.web.views import kelas_views

app_name = "kelas_web"

urlpatterns = [
    path("<int:kelas_id>/", kelas_views.detail_kelas, name="detail_kelas"),
    path("daftar-kelas/", kelas_views.daftar_kelas, name="daftar_kelas"),
    path("daftar-materi/", kelas_views.daftar_materi, name="daftar_materi"),
]