from django.db import models

class JenisPenugasan(models.TextChoices):
    TUGAS = "TUGAS", "Tugas"
    KUIS = "KUIS", "Kuis"
    UTS = "UTS", "UTS"
    UAS = "UAS", "UAS"


class StatusPengumpulan(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    DIKUMPULKAN = "DIKUMPULKAN", "Dikumpulkan"
    DIBATALKAN = "DIBATALKAN", "Dibatalkan"

class Penugasan(models.Model):
    
    kelas = models.ForeignKey(
        "academic.Kelas",
        on_delete=models.CASCADE,
        related_name="penugasan",
    )
    
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)

    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_dibuka = models.DateTimeField()
    batas_pengumpulan = models.DateTimeField()

    jenis = models.CharField(
        max_length=10,
        choices=JenisPenugasan.choices,
    )

    file_url = models.URLField(blank=True)

    def __str__(self):
        return self.judul


class PengumpulanTugas(models.Model):
    penugasan = models.ForeignKey(
        Penugasan,
        on_delete=models.CASCADE,
        related_name="pengumpulan_tugas",
    )
    mahasiswa = models.ForeignKey(
        "accounts.Mahasiswa",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    tanggal_kirim = models.DateTimeField(auto_now_add=True)

    file_url = models.URLField()

    catatan = models.TextField(blank=True)

    status = models.CharField(
        max_length=15,
        choices=StatusPengumpulan.choices,
        default=StatusPengumpulan.DRAFT,
    )

    def __str__(self):
        return f"Pengumpulan #{self.pk}"
