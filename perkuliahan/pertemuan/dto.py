from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

class StatusKehadiran(StrEnum):
    HADIR = "hadir"
    TANPA_KETERANGAN = "tanpa_keterangan"
    IZIN = "izin"
    SAKIT = "sakit"
    
class StatusVerifikasi(StrEnum):
    MENUNGGU = "menunggu"
    DITERIMA = "diterima"
    DITOLAK = "ditolak"
    
# @dataclass(frozen=True)
# class VerifikasiKehadiranDTO:
#     status_kehadiran: StatusKehadiran
#     status_verifikasi: StatusVerifikasi

@dataclass(frozen=True)
class KirimTugasDTO:
    url: str | None = None
    keterangan: str | None = None
    by_kehadiran: bool = False

@dataclass(frozen=True)
class KehadiranDTO:
    mahasiswa_id: int
    statusKehadiran: StatusKehadiran
    statusVerifikasiKehadiran: StatusVerifikasi
    keterangan: str
    tanggal: datetime
    
@dataclass(frozen=True)
class PertemuanIsiKehadiranDTO:
    status_kehadiran: StatusKehadiran
    keterangan: str | None = None
    
@dataclass(frozen=True)
class VerifikasiKehadiranDTO:
    status_verifikasi: StatusVerifikasi
    
@dataclass(frozen=True)
class VerifikasiBanyakKehadiranDTO:
    kehadiran_ids: list[int]
    status_verifikasi: StatusVerifikasi

@dataclass(frozen=True)
class PertemuanDTO:
    pertemuan_ke: int
    nama: str
    mulai: datetime
    selesai: datetime
    # kelas_id: int
    
@dataclass(frozen=True)
class UploadTugasDTO:
    deadline: datetime
    bobot: int = 0
    nama: str | None = None
    url: str | None = None
    by_kehadiran: bool = False
    
@dataclass(frozen=True)
class NilaiTugasDTO:
    nilai: int
    catatan: str | None = None
    
@dataclass(frozen=True)
class FilterKehadiranDTO:
    status_kehadiran: StatusKehadiran | None = None
    status_verifikasi: StatusVerifikasi | None = None

@dataclass(frozen=True)
class EditTugasDTO:
    deadline: datetime
    bobot: int
    by_kehadiran: bool
    nama: str | None = None
    url: str | None = None