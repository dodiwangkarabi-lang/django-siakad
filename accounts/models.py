from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    JENIS_KELAMIN = (
        ("Laki-laki", "Laki-laki"),
        ("Perempuan", "Perempuan"),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    nama = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    no_hp = models.CharField(max_length=20, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    tempat_lahir = models.CharField(max_length=100, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=100, choices=JENIS_KELAMIN, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
class Mahasiswa(BaseModel):
    STATUS = (
        ("Aktif", "Aktif"),
        ("Tidak Aktif", "Tidak Aktif"),
        ("Drop Out", "Drop Out"),
        ("Lulus", "Lulus"),
        ("Cuti", "Cuti")
    )
    
    nim = models.CharField(max_length=10, null=True, blank=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True)
    prodi = models.ForeignKey('academic.Prodi', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nama} - {self.nim}"

class Dosen(BaseModel):
    nip = models.CharField(max_length=10, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.nama} - {self.nip}"