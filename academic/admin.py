from django.contrib import admin
from .models import KRS, DetailKRS, Kelas, MataKuliah, Prodi, Fakultas

admin.site.register(KRS)
admin.site.register(DetailKRS)
admin.site.register(Kelas)
admin.site.register(MataKuliah)
admin.site.register(Prodi)
admin.site.register(Fakultas)