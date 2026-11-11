from dataclasses import dataclass

@dataclass(frozen=True)
class PertemuanDTO:
    pertemuan_ke: int
    nama: str
    kelas_id: int