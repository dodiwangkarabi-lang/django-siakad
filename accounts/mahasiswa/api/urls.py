app_name = "accounts_mahasiswa_api"

from django.urls import path

from . import views

urlpatterns = [
    path("semua/nim/", views.SemuaNimAPIView.as_view(), name="semua_nim"),
    path("biodata-mahasiswa/", views.BiodataMahasiswaAPIView.as_view(), name="biodata_mahasiswa"),
]