from academic.models import Kelas
# from accounts.models import Mahasiswa

# def get_kelas_diambil_mahasiswa(mahasiswa):
#     return (
#         Kelas.objects.filter(
#             peserta__krs__mahasiswa=mahasiswa
#         ).distinct()
#     )

def get_kelas_by_id(kelas_id):
    return Kelas.objects.get(id=kelas_id)
    
def get_kelas_diambil_mahasiswa(mahasiswa_id):
    return (
        Kelas.objects
        .filter(peserta__krs__mahasiswa_id=mahasiswa_id)
        .distinct()
    )