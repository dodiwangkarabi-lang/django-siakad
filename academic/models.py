from django.db import models
from accounts.models import Dosen, Mahasiswa


# ----- choices -----
class SemesterType(models.TextChoices):
    GANJIL = "ganjil", "ganjil"
    GENAP = "genap", "genap"


class SemesterLevel(models.IntegerChoices):
    I = 1, "I"
    II = 2, "II"
    III = 3, "III"
    IV = 4, "IV"
    V = 5, "V"
    VI = 6, "VI"
    VII = 7, "VII"
    VIII = 8, "VIII"
    IX = 9, "IX"
    X = 10, "X"
    XI = 11, "XI"
    XII = 12, "XII"
    XIII = 13, "XIII"
    XIV = 14, "XIV"
    SEMESTER_KHUSUS = 99, "Semester Khusus"


class StatusKRS(models.TextChoices):
    DRAFT = "draft", "draft"
    DIAJUKAN = "diajukan", "diajukan"
    DISETUJUI = "disetujui", "disetujui"
    DITOLAK = "ditolak", "ditolak"
    SELESAI = "selesai", "selesai"
    DIBATALKAN = "dibatalkan", "dibatalkan"


# ----- end choices -----


class Fakultas(models.Model):
    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Prodi(models.Model):
    fakultas = models.ForeignKey(
        Fakultas, on_delete=models.CASCADE, null=True, blank=True
    )

    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class MataKuliah(models.Model):
    class Jenis(models.TextChoices):
        REGULER = "reguler", "Reguler"
        SOFTWARE_ENGINEER = "software_engineer", "Software Engineer"
        HARDWARE_ENGINEER = "hardware_engineer", "Hardware Engineer"
        DIGITAL_ENTERPRENEUR = "digital_enterpreneur", "Digital Enterpreneur"
        MULTIMEDIA = "multimedia", "Multimedia"
        LAINNYA = "lainnya", "Lainnya"

    kode = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    sks = models.IntegerField(null=True, blank=True)
    semester = models.IntegerField(choices=SemesterLevel, null=True, blank=True)
    jenis = models.CharField(
        max_length=20, choices=Jenis.choices, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # sorting
    class Meta:
        ordering = ["nama"]

    def __str__(self):
        return f"{self.nama} - {self.kode}"


class Kelas(models.Model):
    mata_kuliah = models.ForeignKey(
        MataKuliah, on_delete=models.CASCADE, null=True, blank=True
    )
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, null=True, blank=True)

    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    ruangan = models.CharField(max_length=100, null=True, blank=True)
    waktu = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.kode} - {self.nama}"


class KRS(models.Model):
    # SEMESTER = (
    #     ("ganjil", "ganjil"),
    #     ("genap", "genap"),
    # )

    # STATUS = (
    #     ("draft", "draft"),
    #     ("diajukan", "diajukan"),
    #     ("disetujui", "disetujui"),
    #     ("ditolak", "ditolak"),
    #     ("selesai", "selesai"),
    #     ("dibatalkan", "dibatalkan"),
    # )

    mahasiswa = models.ForeignKey(
        Mahasiswa, on_delete=models.CASCADE, null=True, blank=True
    )

    tahun_ajaran = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(
        max_length=10, choices=SemesterType, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=StatusKRS, null=True, blank=True)
    keterangan = models.CharField(max_length=20, default="", null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mahasiswa", "tahun_ajaran", "semester"],
                name="unique_krs_mahasiswa_tahun_ajaran_semester",
            )
        ]

    def __str__(self):
        return (
            f"{self.id} - {self.mahasiswa.nim} - {self.tahun_ajaran} - {self.semester}"
        )


class DetailKRS(models.Model):
    krs = models.ForeignKey(
        KRS, on_delete=models.CASCADE, null=True, blank=True, related_name="detail"
    )
    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE, null=True, blank=True, related_name="peserta"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["krs", "kelas"]
        ordering = ["-updated_at"]

    def __str__(self):
        # return f"{self.krs.mahasiswa.nim} - {self.kelas.mata_kuliah.nama} - {self.krs} - {self.kelas}"
        return f"{self.id}"


class Nilai(models.Model):
    detail_krs = models.OneToOneField(
        DetailKRS, on_delete=models.CASCADE, null=True, blank=True
    )
    nilai_angka = models.FloatField(null=True, blank=True)
    nilai_huruf = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nilai_angka__gte=0, nilai_angka__lte=100),
                name="nilai_angka_antara_0_dan_100",
            )
        ]

    def __str__(self):
        return f"{self.id}"


class KomponenNilai(models.Model):
    PILIHAN = (
        ("UTS", "UTS"),
        ("UAS", "UAS"),
        ("Tugas", "Tugas"),
        ("Kuis", "Kuis"),
        ("Praktikum", "Praktikum"),
        ("Latihan", "Latihan"),
        ("Lainnya", "Lainnya"),
    )

    nama = models.CharField(max_length=100, null=True, blank=True, choices=PILIHAN)
    bobot = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(bobot__gte=0, bobot__lte=100),
                name="bobot_antara_0_dan_100",
            )
        ]

    def __str__(self):
        return f"{self.nama} - {self.bobot}"


class NilaiKomponen(models.Model):
    nilai_id = models.ForeignKey(Nilai, on_delete=models.CASCADE, null=True, blank=True)
    komponen_nilai = models.ForeignKey(
        KomponenNilai, on_delete=models.CASCADE, null=True, blank=True
    )
    nilai = models.FloatField(null=True, blank=True, default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nilai__gte=0, nilai__lte=100),
                name="nilai_antara_0_dan_100",
            ),
            models.UniqueConstraint(
                fields=["nilai_id", "komponen_nilai"], name="unique_nilai_komponen"
            ),
        ]

    def __str__(self):
        return f"{self.nilai_id.detail_krs.krs.mahasiswa.nim} - {self.nilai_id.detail_krs.kelas.mata_kuliah.nama} - {self.nilai_id.detail_krs.krs} - {self.nilai_id.detail_krs.kelas}"


class Kurikulum(models.Model):
    program_studi = models.ForeignKey(
        Prodi, on_delete=models.CASCADE, null=True, blank=True
    )
    tahun = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(
        max_length=10, choices=SemesterType, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.tahun} - {self.semester}"


class KurikulumMataKuliah(models.Model):
    SIFAT = (("wajib", "wajib"), ("pilihan", "pilihan"), ("khusus", "khusus"))

    kurikulum = models.ForeignKey(
        Kurikulum, on_delete=models.CASCADE, null=True, blank=True
    )
    mata_kuliah = models.ForeignKey(
        MataKuliah, on_delete=models.CASCADE, null=True, blank=True
    )
    sifat = models.CharField(max_length=20, choices=SIFAT, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["kurikulum", "mata_kuliah"], name="unique_kurikulum_mata_kuliah"
            )
        ]

    def __str__(self):
        return f"{self.id}"


class PeriodeKRS(models.Model):
    STATUS = (("aktif", "aktif"), ("nonaktif", "nonaktif"))

    tahun_ajaran = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(
        max_length=10, choices=SemesterType, null=True, blank=True
    )
    tanggal_mulai = models.DateField(null=True, blank=True)
    tanggal_selesai = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True)
    
    # file
    template = models.FileField(upload_to="krs/template", null=True, blank=True)
    template_meta_field = models.FileField(upload_to="krs/template", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tahun_ajaran", "semester"], name="unique_tahun_ajaran_semester"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(tanggal_mulai__isnull=True)
                    | models.Q(tanggal_selesai__isnull=True)
                    | models.Q(tanggal_selesai__gte=models.F("tanggal_mulai"))
                ),
                name="tanggal_mulai_lebih_kecil_dari_tanggal_selesai",
            ),
            models.UniqueConstraint(
                fields=["status"],
                condition=models.Q(status="aktif"),
                name="unique_periode_krs_aktif",
            ),
        ]

    def __str__(self):
        return f"{self.id} - {self.tahun_ajaran} - {self.semester}"


class PenawaranKRS(models.Model):
    periode_krs = models.ForeignKey(
        PeriodeKRS, on_delete=models.CASCADE, null=True, blank=True
    )
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, null=True, blank=True)
    kuota = models.IntegerField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["periode_krs", "kelas"], name="unique_periode_krs_kelas"
            )
        ]

    def __str__(self):
        return f"{self.id} - {self.periode_krs} - {self.kelas}"
