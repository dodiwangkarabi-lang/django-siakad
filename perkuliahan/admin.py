from django.contrib import admin
from .models import (
    Kehadiran, Pertemuan,
    Tugas, KumpulTugas,
    Nilai
)

# register pertemuan site
admin.site.register(Pertemuan)
admin.site.register(Tugas)
admin.site.register(KumpulTugas)
admin.site.register(Nilai)

@admin.register(Kehadiran)
class KehadiranAdmin(admin.ModelAdmin):
    readonly_fields = ("tanggal",)
    