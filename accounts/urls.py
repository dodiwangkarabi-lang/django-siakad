from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("dosen", views.DosenViewSet)
router.register("mahasiswa", views.MahasiswaViewSet)
router.register("user", views.UserViewSet)

urlpatterns = [
    # mahasiswa
    path("api/mahasiswa/", include("accounts.mahasiswa.api.urls", namespace="accounts_mahasiswa_api")),
    
    path("api/", include(router.urls)),
    
]