from django.contrib import admin
from .models import Dosen, Mahasiswa, TandaTangan

admin.site.register(Dosen)
# admin.site.register(TandaTangan)

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    ordering = ["nama"] # ascending
    search_fields = ["nim", "nama"]
    # ordering = ["-nama"] # descending
    
@admin.register(TandaTangan)
class TandaTanganAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "nama"]
    

