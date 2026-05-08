from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("dosen", views.DosenViewSet)
router.register("mahasiswa", views.MahasiswaViewSet)
router.register("user", views.UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]