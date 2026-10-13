from dataclasses import dataclass
from academic.krs.dto.mhs_dto import SemesterType
from typing import Any
# from enum import StrEnum

# class SemesterType(StrEnum):
#     GANJIL = "ganjil"
#     GENAP = "genap"

@dataclass
class Pesan:
    status: bool
    pesan: str
    
@dataclass
class Result:
    is_success: bool
    data: Any | None = None
    errors: dict[str, list[str]] | None = None
    
@dataclass
class GenerateBanyakKRSRequest:
    daftar_nim: list[str]
    tahun_ajaran: str
    semester: SemesterType