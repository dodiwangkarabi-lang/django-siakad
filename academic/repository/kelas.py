from academic.models import Kelas
from typing import TypedDict

class KelasType(TypedDict):
    kode: str
    nama: str
    ruangan: str
    waktu: str
    
    dosen_id: int
    mata_kuliah_id: int

class KelasRepository:
    def __init__(self):
        self.model = Kelas
        
    def get_by_id(self, id: int) -> Kelas | None:
        return self.model.objects.filter(id=id).first()
    
    def get_all(self) -> list[Kelas] | None:
        return self.model.objects.all()
    
    def create(self, data: KelasType) -> Kelas:
        return self.model.objects.create(**data)
    
    def update(self, id: int, data: KelasType) -> Kelas:
        return self.model.objects.filter(id=id).update(**data)
    
    def delete(self, id: int) -> None:
        return self.model.objects.filter(id=id).delete()