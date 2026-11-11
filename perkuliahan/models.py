from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from academic.models import (
    Kelas
)

from accounts.models import (
    Dosen, Mahasiswa
)

class Pertemuan(models.Model):
    pertemuan_ke = models.IntegerField(null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, null=True, blank=True)
    mulai = models.DateTimeField(null=True, blank=True)
    selesai = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pertemuan_ke', 'kelas'], name='unique_pertemuan_ke'),
        ]
    
    def __str__(self):
        return f"{self.pertemuan_ke} - {self.kelas}"
    
class StatusKehadiran(models.TextChoices):
    HADIR = "hadir"
    TANPA_KETERANGAN = "tanpa_keterangan"
    IZIN = "izin"
    SAKIT = "sakit"
    
class StatusVerifikasiKehadiran(models.TextChoices):
    MENUNGGU = "menunggu"
    DITERIMA = "diterima"
    DITOLAK = "ditolak"
    
    
class Kehadiran(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, null=True, blank=True)
    pertemuan = models.ForeignKey(Pertemuan, on_delete=models.CASCADE, null=True, blank=True)
    status_kehadiran = models.CharField(max_length=20, choices=StatusKehadiran, null=True, blank=True)
    status_verifikasi = models.CharField(max_length=20, choices=StatusVerifikasiKehadiran, null=True, blank=True)
    keterangan = models.CharField(max_length=100, null=True, blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mahasiswa', 'pertemuan'], name='unique_mahasiswa_pertemuan'),
        ]
    
    def __str__(self):
        return f"{self.id} {self.mahasiswa} - {self.pertemuan}"
    
class Tugas(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    bobot = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    url = models.CharField(max_length=200, null=True, blank=True)
    by_kehadiran = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.nama}"
    
class Materi(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, on_delete=models.CASCADE, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    keterangan = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pertemuan} - {self.nama}"
    
class KumpulTugas(models.Model):
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE, null=True, blank=True)
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    keterangan = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tugas', 'mahasiswa'], name='unique_tugas_mahasiswa'),
        ]
    
    def __str__(self):
        return f"<id: {self.id}> tugas id: {self.tugas.id} - mhs_id: {self.mahasiswa.id}"
    
class Nilai(models.Model):
    nilai = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    catatan = models.CharField(max_length=100, null=True, blank=True)
    kumpul_tugas = models.OneToOneField(KumpulTugas, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"id: {self.id} - tugas: {self.kumpul_tugas.id} - {self.nilai}"