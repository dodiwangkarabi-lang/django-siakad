from django.urls import path, include
app_name = "perkuliahan_api"

urlpatterns = [
    path("pertemuan/", include("perkuliahan.pertemuan.api.urls", namespace="perkuliahan_pertemuan_api")),
]
