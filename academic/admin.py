from django.contrib import admin
from .models import (
    KRS, DetailKRS, Kelas, MataKuliah, Prodi, Fakultas,
    Nilai, NilaiKomponen, KomponenNilai,
    Kurikulum, KurikulumMataKuliah,
    PeriodeKRS, PenawaranKRS
)

admin.site.register(KRS)
admin.site.register(DetailKRS)
admin.site.register(Kelas)
admin.site.register(MataKuliah)
admin.site.register(Prodi)
admin.site.register(Fakultas)

admin.site.register(Nilai)
admin.site.register(NilaiKomponen)
admin.site.register(KomponenNilai)

admin.site.register(Kurikulum)
admin.site.register(KurikulumMataKuliah)

admin.site.register(PeriodeKRS)
admin.site.register(PenawaranKRS)