from accounts.models import (
    Mahasiswa
)

from core import dto

class MahasiswaService:
    
    @staticmethod
    def getNimList(**kwargs) -> dto.Result:
       mahasiswa_qs = Mahasiswa.objects.all().filter(**kwargs).values_list("nim", flat=True)
       return dto.Result(is_success=True, data=mahasiswa_qs)
   
    @staticmethod
    def getNimNamaList(**kwargs) -> dto.Result:
        mahasiswa_qs = (
            Mahasiswa.objects.all()
            .filter(**kwargs)
            # .values_list("nim", "nama", flat=False)
            .values("nim", "nama")
        )
        return dto.Result(is_success=True, data=mahasiswa_qs)
    
    @staticmethod
    def biodata(**kwargs) -> dto.Result:
        nim = kwargs.get("nim")
        if nim:
            mahasiswa = MahasiswaService.get_by_nim(nim)
            if mahasiswa is None:
                return dto.Result(is_success=False, errors={"nim": ["nim tidak ditemukan"]})
            return dto.Result(is_success=True, data=mahasiswa)
        
        mahasiswa_id = kwargs.get("id")
        if mahasiswa_id:
            mahasiswa = MahasiswaService.get_by_id(mahasiswa_id)
            if mahasiswa is None:
                return dto.Result(is_success=False, errors={"id": ["id tidak ditemukan"]})
            return dto.Result(is_success=True, data=mahasiswa)
        
        return dto.Result(is_success=False, errors={"non_field_errors": ["nim atau id harus diisi"]})
    
    @staticmethod
    def get_by_nim(nim: str) -> Mahasiswa | None:
        return Mahasiswa.objects.filter(nim=nim).first()
    
    @staticmethod
    def get_by_id(id: int) -> Mahasiswa | None:
        return Mahasiswa.objects.filter(id=id).first()
    
    @staticmethod
    def get_all_by_nim(nim_list: list) -> list:
        return Mahasiswa.objects.filter(nim__in=nim_list)