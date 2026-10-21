from django.urls import path, include

app_name = "academic_kelola_kelas_api"

urlpatterns = [
    path("jadwal/", include("academic.kelola_kelas.jadwal.urls", namespace="jadwal_api")),
]
