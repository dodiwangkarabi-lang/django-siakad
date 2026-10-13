from ..exceptions.exceptions import KRSException
from academic import models

class KRSRules:
    
    @staticmethod
    def ensure_owner(krs, mahasiswa_id):
        if krs.mahasiswa.id != mahasiswa_id:
            raise KRSException(message="ini bukan krs anda", field="non_field_errors")
        
    
    @staticmethod
    def ensure_can_submit(krs):
        if krs.status not in (
            models.StatusKRS.DRAFT,
            models.StatusKRS.DITOLAK
        ):
            raise KRSException(message="status tidak valid", field="non_field_errors")
        
    @staticmethod
    def ensure_can_cetak(krs):
        if krs.status != models.StatusKRS.DISETUJUI:
            raise KRSException(message="status tidak valid", field="non_field_errors")