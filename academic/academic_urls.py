from django.urls import path, include

from . import views

app_name = "academic"

urlpatterns = [
    # path("api/", include("academic.api.urls")),
    path("kelas/", include("academic.web.urls.kelas_urls")),
    
]