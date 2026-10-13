from .krs import KRSRepository
from .mahasiswa import MahasiswaRepository
from .detail_krs import DetailKRSRepository
from .kelas import KelasRepository
from .mata_kuliah import MataKuliahRepository

__all__ = [
    "KRSRepository", "MahasiswaRepository", "DetailKRSRepository",
    "KelasRepository", "MataKuliahRepository"
]