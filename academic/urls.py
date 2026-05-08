from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("krs", views.KRSView)
router.register("detailkrs", views.DetailKRSView)
router.register("kelas", views.KelasView)
router.register("matkul", views.MataKuliahView)
router.register("prodi", views.ProdiView)
router.register("fakultas", views.FakultasView)

urlpatterns = [
    path("api/detail/", views.DetailKRSAPIView.as_view(), name="index"),
    path("api/", include(router.urls)),
]