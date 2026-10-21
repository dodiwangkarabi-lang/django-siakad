class Slot:
    def __init__(self, field: str):
        self.field = field
        
class KelasSlot:
    def __init__(self, kelas_id: int, field: str):
        self.kelas_id = kelas_id
        self.field = field
        
    def pindahkan(self, kelas_id: int, field: str):
        self.kelas_id = kelas_id
        self.field = field
        
    def hapus(self):
        self.kelas_id = None
        
    def is_empty(self):
        return self.kelas_id is None