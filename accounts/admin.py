from django.contrib import admin
from .models import Dosen, Mahasiswa

admin.site.register(Dosen)

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    ordering = ["nama"] # ascending
    # ordering = ["-nama"] # descending
