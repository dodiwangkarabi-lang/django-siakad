from .dto import *
from .errors import error_generate
from academic import models

class ValidasiKRS:
    def __init__(self):
        pass
    
    def daftar_krs_diajukan(self) -> ResultDTO:
        daftar_krs = (
            models.KRS.objects
            .filter(status=models.StatusKRS.DIAJUKAN)
        )
        
        return ResultDTO(
            is_success=True, data=daftar_krs
        )
    
    def validasi(self, krs_id, status, keterangan="") -> ResultDTO:
        
        krs = models.KRS.objects.filter(id=krs_id).first()
        err = {}
        if not krs:
            err = error_generate(key="non_field_errors", value=["krs tidak ditemukan"])
            return ResultDTO(
                is_success=False, errors=err
            )
            
        if krs.status != models.StatusKRS.DIAJUKAN:
            return ResultDTO(is_success=False, errors={"non_field_errors": ["status tidak valid (bukan diajukan)"]})
        
        
        # validasi statu harus ada dalam list StatusKRS
        if status not in models.StatusKRS:
            return ResultDTO(is_success=False, errors={"non_field_errors": ["status tidak valid"]})
        
        krs.status = status
        krs.keterangan = keterangan
        krs.save()
        return ResultDTO(
            is_success=True,
            messages="berhasil update status"
        )