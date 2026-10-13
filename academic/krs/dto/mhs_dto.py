from dataclasses import dataclass
# from .dto import SemesterType
from academic.models import SemesterType
from typing import List

@dataclass
class BuatKrs:
    nim: str
    tahun_ajaran: str
    semester: SemesterType

@dataclass
class TambahKelas:
    krs_id: int
    kelas_id: int
    
@dataclass
class TambahBanyakKelas:
    krs_id: int
    kelas_ids: List[int]
    
@dataclass
class HapusKelas:
    kelas_id: int
    
@dataclass
class SimpanDraft:
    krs_id: int
    
@dataclass
class AjukanKRS:
    krs_id: int