from django.urls import path

app_name = "jadwal_api"

from . import views

urlpatterns = [
    path("jadwal/", views.JadwalAPIView.as_view(), name="jadwal"),
    path("download-jadwal/", views.DownloadJadwalAPIView.as_view(), name="download_jadwal"),
    path("kelas-list/", views.KelasListAPIView.as_view(), name="kelas_list"),
    path("dosen-pengampu/", views.DosenPengampuAPIView.as_view(), name="dosen_pengampu"),
    path("set-dosen-pengampu/<int:kelas_id>/", views.SetDosenPengampuAPIView.as_view(), name="set_dosen_pengampu"),
    path("hapus-dosen-pengampu/<int:kelas_id>/", views.HapusDosenPengampuAPIView.as_view(), name="hapus_dosen_pengampu"),
]