import typing
from academic.models import DetailKRS


class DetailKRSType(typing.TypedDict):
    krs_id: int
    kelas_id: int
    

class DetailKRSRepository:
    def __init__(self):
        self.model = DetailKRS
        
    def get_by_id(self, id: int) -> DetailKRS | None:
        return self.model.objects.filter(id=id).first()
    
    def get_all(self) -> list[DetailKRS] | None:
        return self.model.objects.all()
    
    def create(self, data: DetailKRSType) -> DetailKRS:
        return self.model.objects.create(**data)
    
    def update(self, id: int, data: DetailKRSType) -> DetailKRS:
        return self.model.objects.filter(id=id).update(**data)
    
    def delete(self, id: int) -> None:
        return self.model.objects.filter(id=id).delete()