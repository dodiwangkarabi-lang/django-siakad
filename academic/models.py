from django.db import models
from accounts.models import Dosen, Mahasiswa

class Fakultas(models.Model):
    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"

class Prodi(models.Model):
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE, null=True, blank=True)
    
    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"
    

class MataKuliah(models.Model):
    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    sks = models.IntegerField(null=True, blank=True)
    semester = models.CharField(max_length=10, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"{self.nama} - {self.kode}"
    
class Kelas(models.Model):
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, null=True, blank=True)
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, null=True, blank=True)
    
    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    ruangan = models.CharField(max_length=100, null=True, blank=True)
    waktu = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.pk} - {self.kode} - {self.nama}"
    
class KRS(models.Model):
    SEMESTER = (
        ("ganjil", "ganjil"),
        ("genap", "genap"),
    )
    
    
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, null=True, blank=True)
    
    tahun_ajaran = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(max_length=10, choices=SEMESTER, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.mahasiswa.nim} - {self.tahun_ajaran} - {self.semester}"
    
class DetailKRS(models.Model):
    krs = models.ForeignKey(KRS, on_delete=models.CASCADE, null=True, blank=True, related_name="detail")
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, null=True, blank=True, related_name="peserta")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['krs', 'kelas']
    
    def __str__(self):
        return f"{self.krs.mahasiswa.nim} - {self.kelas.mata_kuliah.nama} - {self.krs} - {self.kelas}"