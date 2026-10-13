from accounts.models import (
    Dosen, Mahasiswa
)

class MahasiswaRepository:
    def __init__(self):
        self.model = Mahasiswa
        
    def get_by_nim(self, nim: str) -> Mahasiswa | None:
        return self.model.objects.filter(nim=nim).first()