from dataclasses import dataclass
import typing

T = typing.TypeVar("T")

@dataclass(frozen=True)
class AjukanBanyakKelasParamsDTO:
    mahasiswa_ids: list[int]
    kelas_ids: list[int]
    
@dataclass(frozen=True)
class AjukanBanyakKelasResultDTO(typing.Generic[T]):
    is_success: bool
    message: str | None = None
    errors: list[dict[str, list[str]]] | None = None
    data: T | None = None
    
@dataclass(frozen=True)
class Result(typing.Generic[T]):
    is_success: bool
    message: str | None = None
    errors: list[dict[str, list[str]]] | None = None
    data: T | None = None