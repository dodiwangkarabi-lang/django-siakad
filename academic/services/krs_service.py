from academic.models import (
    Mahasiswa, KRS, DetailKRS
)

class KRSMahasiswaService:
    def __init__(self, krs_repo, mahasiswa_repo):
        self.krs_repo = krs_repo
        self.mahasiswa_repo = mahasiswa_repo

    def lihat_krs_aktif(self, nim: str, tahun_ajaran: str, semester: str) -> KRS | None:
        mahasiswa = self.mahasiswa_repo.get_by_nim(nim)
        if not mahasiswa:
            return None
        
        hasil = KRS.objects.filter(
            mahasiswa=mahasiswa, tahun_ajaran=tahun_ajaran, semester=semester
        ).first()
        return hasil
    
class KRSDosenService:
    def __init__(self):
        pass

class KRSTuService:
    def __init__(self):
        pass