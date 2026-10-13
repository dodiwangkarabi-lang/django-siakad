from academic.models import MataKuliah
import typing
from enum import StrEnum

class Jenis(StrEnum):
    REGULER = "reguler"
    SOFTWARE_ENGINEER = "software_engineer"
    HARDWARE_ENGINEER = "hardware_engineer"
    DIGITAL_ENTERPRENEUR = "digital_enterpreneur"
    MULTIMEDIA = "multimedia"
    LAINNYA = "lainnya"

class MahasiswaType(typing.TypedDict):
    kode: str
    nama: str
    sks: int
    semester: int
    jenis: Jenis
    
class MataKuliahRepository:
    def __init__(self):
        self.model = MataKuliah
        
    def get_by_id(self, id: int) -> MataKuliah | None:
        return self.model.objects.filter(id=id).first()
    
    def get_all(self) -> list[MataKuliah] | None:
        return self.model.objects.all()
    
    def create(self, data: MahasiswaType) -> MataKuliah:
        return self.model.objects.create(**data)
    
    def update(self, id: int, data: MahasiswaType) -> MataKuliah:
        return self.model.objects.filter(id=id).update(**data)
    
    def delete(self, id: int) -> None:
        return self.model.objects.filter(id=id).delete()