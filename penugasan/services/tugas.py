from penugasan.models import (
    Penugasan, PengumpulanTugas
)

from accounts.models import Mahasiswa

def kirim_tugas(*, penugasan: Penugasan, mahasiswa: Mahasiswa, data: dict):
    """
    kirim tugas oleh Mahasiswa

    Args:
        penugasan (Penugasan): instance Penugasan
        mahasiswa (Mahasiswa): instance Mahasiswa
        data (dict): data cleaned, keynya:
                file_url
                catatan

    Returns:
        _type_: _description_
    """
    PengumpulanTugas.objects.create(penugasan=penugasan, mahasiswa=mahasiswa, **data)
    return True

def buat_tugas():
    pass