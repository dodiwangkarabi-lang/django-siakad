from dataclasses import dataclass
import typing

T = typing.TypeVar("T")


@dataclass(frozen=True)
class Result:
    is_success: bool
    data: typing.Any | None = None
    errors: dict[str, list[str]] | None = None
    messages: str | None = None
    
@dataclass(frozen=True)
class IsiSlotJadwal:
    field: str
    kelas_id: int
    
@dataclass(frozen=True)
class SetDosenPengampuRequeestDTO:
    kelas_id: int
    dosen_id: int
    
@dataclass(frozen=True)
class DosenPengampuTambahDTO:
    nama: str
    nip: str | None = None
    no_hp: str | None = None