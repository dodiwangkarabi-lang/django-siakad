from django.db import transaction
from django.db.models import F, Sum

from penugasan.services import tugas
from perkuliahan.models import (
    Pertemuan, Kelas, Tugas, Kehadiran, KumpulTugas,
    Mahasiswa, Dosen,
    Nilai
)

from perkuliahan.pertemuan import utils

from shared.dto import Result
from . import dto
import datetime

from django.utils import timezone

def isMahasiswa(user) -> bool:
    role = user.groups.filter(name="mahasiswa").exists()
    return role

def isDosen(user) -> bool:
    role = user.groups.filter(name="dosen").exists()
    return role

def get_role(user):
    if isMahasiswa(user):
        return "mahasiswa"
    elif isDosen(user):
        return "dosen"
    else:
        return "unknown"

class NilaiRules:
    @staticmethod
    def rentang_nilai_valid(nilai):
        if nilai > 100:
            raise Exception("Nilai tidak boleh lebih dari 100")
        if nilai < 0:
            raise Exception("Nilai tidak boleh kurang dari 0")

class KumpulTugasRules:
    @staticmethod
    def is_pemilik(*, mahasiswa, kumpul_tugas):
        if kumpul_tugas.mahasiswa != mahasiswa:
            raise Exception("Kumpul tugas bukan milik mahasiswa ini")
        
    @staticmethod
    def is_valid_id(*, kumpul_tugas_id: int):
        kumpul_tugas = KumpulTugas.objects.filter(id=kumpul_tugas_id).first()
        if not kumpul_tugas:
            raise Exception("Kumpul tugas tidak ditemukan")
        return kumpul_tugas

class TugasRules:
    @staticmethod
    def tugas_valid(tugas_id):
        tugas = Tugas.objects.filter(id=tugas_id).first()
        if not tugas:
            raise Exception("Tugas tidak ditemukan")
        return tugas
    
    @staticmethod
    def kumpul_tugas_valid(kumpul_tugas_id):
        kumpul_tugas = KumpulTugas.objects.filter(id=kumpul_tugas_id).first()
        if not kumpul_tugas:
            raise Exception("Kumpul tugas tidak ditemukan")
        return kumpul_tugas
    
    @staticmethod
    def mahasiswa_sudah_kumpul_tugas(tugas_id, mahasiswa):
        tugas_kumpul = KumpulTugas.objects.filter(tugas_id=tugas_id, mahasiswa=mahasiswa).first()
        if not tugas_kumpul:
            raise Exception("Mahasiswa belum mengumpulkan tugas ini")
        return tugas_kumpul
    
    @staticmethod
    def sudah_deadline(tugas:Tugas):
        now = timezone.now()
        if tugas.deadline < now:
            raise Exception("Tugas sudah melewati deadline")

class AkunRules:
    @staticmethod
    def mahasiswa_valid(mahasiswa_id):
        mahasiswa = Mahasiswa.objects.filter(id=mahasiswa_id).first()
        if not mahasiswa:
            raise Exception("Mahasiswa tidak ditemukan")
        return mahasiswa
    
    @staticmethod
    def dosen_valid(dosen_id):
        dosen = Dosen.objects.filter(id=dosen_id).first()
        if not dosen:
            raise Exception("Dosen tidak ditemukan")
        return dosen
    
    @staticmethod
    def is_mahasiswa(user) -> None:
        role = isMahasiswa(user)
        if not role:
            raise Exception("User bukan mahasiswa")
        
    @staticmethod
    def is_dosen(user) -> None:
        role = isDosen(user)
        if not role:
            raise Exception("User bukan dosen")

class KehadiranRules:
    
    @staticmethod
    def hadiri_pertemuan(*, mahasiswa, pertemuan) -> None:
        pesan = "Anda tidak mengikuti pertemuan ini"
        kehadiran = Kehadiran.objects.filter(mahasiswa=mahasiswa, pertemuan=pertemuan).first()
        if not kehadiran:
            raise Exception(pesan)
        
        if kehadiran.status_kehadiran != "hadir" or kehadiran.status_verifikasi != "diterima":
            raise Exception(pesan)
    
    @staticmethod
    def is_mahasiswa(user) -> None:
        role = isMahasiswa(user)
        if not role:
            raise Exception("User bukan mahasiswa")
        
    @staticmethod
    def kelas_selesai(pertemuan: Pertemuan) -> None:
        if not pertemuan.selesai:
            raise Exception("waktu belum di atur")
        
        if pertemuan.selesai < timezone.now():
            raise Exception("Pertemuan sudah selesai")
        
    @staticmethod
    def is_dosen(user) -> None:
        role = isDosen(user)
        if not role:
            raise Exception("User bukan dosen")
        
    # @staticmethod
    # def tergabung_dalam_kelas(user, pertemuan_id) -> None:
    #     pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
    #     kelas = pertemuan.kelas
    #     mahasiswa = user.mahasiswa
    #     if not kelas:
    #         raise Exception("belum tergabung dalam kelas")
        
    
    @staticmethod
    def pertemuan_valid(pertemuan_id):
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            raise Exception("Pertemuan tidak ditemukan")
        return pertemuan
    
    @staticmethod
    def kelas_valid(kelas_id):
        kelas = Kelas.objects.filter(id=kelas_id).first()
        if not kelas:
            raise Exception("Kelas tidak ditemukan")
        return kelas
    
    @staticmethod
    def kehadiran_valid(kehadiran_id):
        kehadiran = Kehadiran.objects.filter(id=kehadiran_id).first()
        if not kehadiran:
            raise Exception("Kehadiran tidak ditemukan")
        return kehadiran
    
    @staticmethod
    def status_verifikasi_bukan_menunggu(kehadiran):
        # kehadiran = Kehadiran.objects.filter(id=kehadiran_id).first()
        if kehadiran.status_verifikasi != dto.StatusVerifikasi.MENUNGGU:
            raise Exception("Status verifikasi bukan menunggu")
        # return kehadiran
        
class NilaiService:
    
    @staticmethod
    def lihat_nilai_tugas(*, user, kelas_id: int) -> Result:
        try:
            kelas = KelasService.kelas_valid(kelas_id)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        role = get_role(user)
        if role == "dosen":
            qs = (
                KumpulTugas.objects
                .filter(tugas__pertemuan__kelas=kelas)
                .select_related("mahasiswa", "tugas__pertemuan__kelas")
                # .values(
                #     "mahasiswa",
                #     "tugas",
                #     "nilai"
                # )
                .distinct()
            )
            return Result(is_success=True, data=qs)
        
        if role == "mahasiswa":
            qs = (
                KumpulTugas.objects
                .filter(mahasiswa=user.mahasiswa, tugas__pertemuan__kelas=kelas)
                .select_related("mahasiswa", "tugas__pertemuan__kelas")
                # .values(
                #     "mahasiswa",
                #     "tugas",
                #     "nilai"
                # )
                .distinct()
            )
            return Result(is_success=True, data=qs)
        
        return Result(is_success=False, errors={"non_field_errors": ["User bukan dosen atau mahasiswa"]})
    
    @staticmethod
    def hitung_point(*, user, kelas_id: int) -> Result:
        try:
            AkunRules.is_mahasiswa(user)
            kelas = KelasService.kelas_valid(kelas_id)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
            
        mahasiswa = user.mahasiswa
        total_bobot = (
            Tugas.objects
            .filter(pertemuan__kelas=kelas)
            .aggregate(total=Sum('bobot'))
        )['total'] or 0
        
        kumpulan_nilai = (
            Nilai.objects
            .filter(
                kumpul_tugas__mahasiswa=mahasiswa,
                kumpul_tugas__tugas__pertemuan__kelas=kelas
            )
            # .select_related("kumpul_tugas__tugas__pertemuan__kelas", "kumpul_tugas__tugas")
            .values(
                "nilai",
                bobot=F("kumpul_tugas__tugas__bobot")
            )
        )
        hasil = {
            "total_nilai": 0,
            "total_bobot": 0
        }
        for nilai in kumpulan_nilai:
            temp_nilai = utils.nilai_to_point(nilai["nilai"], nilai["bobot"])
            hasil["total_nilai"] += temp_nilai
            # hasil["total_bobot"] += nilai["bobot"]
            
        hasil["total_bobot"] = total_bobot
            
        return Result(is_success=True, data=hasil)

class KelasService:
    def __init__(self):
        pass
    
    
    @staticmethod
    def kelas_by_id(*, kelas_id: int) -> Result:
        kelas = Kelas.objects.select_related("mata_kuliah").filter(id=kelas_id).first()
        if not kelas:
            return Result(is_success=False, errors={"non_field_errors": ["Kelas tidak ditemukan"]})
        return Result(is_success=True, data=kelas)
    
    @staticmethod
    def kelas_valid(kelas_id):
        kelas = Kelas.objects.filter(id=kelas_id).first()
        if not kelas:
            raise Exception("Kelas tidak ditemukan")
        return kelas
    
    @staticmethod
    def get_kelas(*, user) -> Result:
        if isMahasiswa(user):
            mahasiswa = user.mahasiswa
            kelas = (
                Kelas.objects
                .filter(
                    penawarankrs__periode_krs__status="aktif",
                    peserta__krs__mahasiswa=mahasiswa,
                    dosen__nama__icontains="Dodiman",
                )
                .select_related("dosen", "mata_kuliah")
            )
        elif isDosen(user):
            dosen = user.dosen
            kelas = (
                Kelas.objects
                .filter(
                    penawarankrs__periode_krs__status="aktif",
                    dosen__nama__icontains="dodiman",
                )
                .select_related("dosen", "mata_kuliah")
            )
        else:
            return Result(is_success=False, errors={"non_field_errors": ["User bukan mahasiswa atau dosen"]})
        
        return Result(is_success=True, data=kelas, messages="Berhasil mendapatkan kelas")

class KehadiranService:
    def __init__(self):
        pass
    
    @staticmethod
    def daftar_hadir_perlu_konfirmasi(*, pertemuan_id:int, user) -> Result:
        try:
            KehadiranRules.is_dosen(user)
            pertemuan = KehadiranRules.pertemuan_valid(pertemuan_id)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        kehadiran = (
            Kehadiran.objects
            .filter(pertemuan=pertemuan, status_verifikasi=dto.StatusVerifikasi.MENUNGGU)
            .select_related("pertemuan", "mahasiswa")
        )
        return Result(is_success=True, data=kehadiran)
    
    @staticmethod
    def daftar_kehadiran(*, pertemuan_id:int, user, params:dto.FilterKehadiranDTO = None) -> Result:
        try:
            KehadiranRules.is_dosen(user)
            pertemuan = KehadiranRules.pertemuan_valid(pertemuan_id)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        kehadiran = (
            Kehadiran.objects.filter(pertemuan=pertemuan)
            .select_related("pertemuan", "mahasiswa")
        )
        
        # filter by params
        if params and params.status_kehadiran:
            kehadiran = kehadiran.filter(status_kehadiran=params.status_kehadiran)
        if params and params.status_verifikasi:
            kehadiran = kehadiran.filter(status_verifikasi=params.status_verifikasi)
            
        return Result(is_success=True, data=kehadiran)
    
    @staticmethod
    def daftar_kehadiaran_mahasiswa(*, pertemuan_id:int, user) -> Result:
        try:
            KehadiranRules.is_mahasiswa(user)
            pertemuan = KehadiranRules.pertemuan_valid(pertemuan_id)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        kehadiran = Kehadiran.objects.filter(pertemuan=pertemuan, mahasiswa=user.mahasiswa)
        return Result(is_success=True, data=kehadiran)
    
    @staticmethod
    def is_mahasiswa_sudah_isi_kehadiran(*, pertemuan_id:int, user) -> Result:
        try:
            KehadiranRules.is_mahasiswa(user)
            pertemuan = KehadiranRules.pertemuan_valid(pertemuan_id)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        isSudahIsi = (
            Kehadiran.objects
            .filter(pertemuan=pertemuan, mahasiswa=user.mahasiswa)
            .exists()
        )
        return Result(is_success=True, data=isSudahIsi)
    
    @staticmethod
    def kehadiran_siswa_by_kelas(*, kelas_id:int, user) -> Result:
        role = get_role(user)
        if role == "mahasiswa":
            try:
                KehadiranRules.is_mahasiswa(user)
                kelas = KehadiranRules.kelas_valid(kelas_id)
            except Exception as e:
                return Result(is_success=False, errors={"non_field_errors": [str(e)]})
            
            kehadiran = (
                Kehadiran.objects.filter(pertemuan__kelas=kelas, mahasiswa=user.mahasiswa)
                .select_related("pertemuan__kelas", "mahasiswa")
            )
            return Result(is_success=True, data=kehadiran)
        elif role == "dosen":
            try:
                KehadiranRules.is_dosen(user)
                kelas = KehadiranRules.kelas_valid(kelas_id)
            except Exception as e:
                return Result(is_success=False, errors={"non_field_errors": [str(e)]})
            
            kehadiran = (
                Kehadiran.objects.filter(pertemuan__kelas=kelas)
                .select_related("pertemuan__kelas", "mahasiswa")
            )
            return Result(is_success=True, data=kehadiran)
        else:
            return Result(is_success=False, errors={"non_field_errors": ["User bukan mahasiswa atau dosen"]})
    
    @staticmethod
    def isi_kehadiran(*, pertemuan_id:int, user,  data:dto.PertemuanIsiKehadiranDTO) -> Result:
        
        # kumpulan aturan
        try:
            KehadiranRules.is_mahasiswa(user)
            pertemuan = KehadiranRules.pertemuan_valid(pertemuan_id)
            KehadiranRules.kelas_selesai(pertemuan)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        mahasiswa = user.mahasiswa
        
        try:
            kehadiran = Kehadiran.objects.create(
                pertemuan=pertemuan,
                mahasiswa=mahasiswa,
                status_kehadiran=dto.StatusKehadiran(data.status_kehadiran),
                status_verifikasi=dto.StatusVerifikasi.MENUNGGU,
                keterangan=data.keterangan,
                tanggal=timezone.now(),
            )
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        return Result(is_success=True, data=kehadiran)
    
    @staticmethod
    def verifikasi_kehadiran(*,user, kehadiran_id:int, data:dto.VerifikasiKehadiranDTO) -> Result:
        try:
            KehadiranRules.is_dosen(user)
            kehadiran = KehadiranRules.kehadiran_valid(kehadiran_id)
            KehadiranRules.status_verifikasi_bukan_menunggu(kehadiran)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        if data.status_verifikasi == dto.StatusVerifikasi.DITOLAK:
            status_kehadiran = dto.StatusKehadiran.TANPA_KETERANGAN
        elif data.status_verifikasi == dto.StatusVerifikasi.DITERIMA:
            status_kehadiran = kehadiran.status_kehadiran
        
        kehadiran.status_kehadiran = status_kehadiran
        kehadiran.status_verifikasi = data.status_verifikasi
        kehadiran.save()
        return Result(is_success=True, data=kehadiran)
    
    @staticmethod
    def verifikasi_banyak_kehadiran(*,user, pertemuan_id:int, data:dto.VerifikasiBanyakKehadiranDTO) -> Result:
        try:
            pertemuan = KehadiranRules.pertemuan_valid(pertemuan_id)
            KehadiranRules.is_dosen(user)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        # bulk
        kehadiran_list = Kehadiran.objects.filter(id__in=data.kehadiran_ids)
        
        with transaction.atomic():
            for kehadiran in kehadiran_list:
                try:
                    KehadiranRules.status_verifikasi_bukan_menunggu(kehadiran)
                except Exception as e:
                    return Result(is_success=False, errors={"non_field_errors": [str(e)]})
                
                if data.status_verifikasi == dto.StatusVerifikasi.DITOLAK:
                    status_kehadiran = dto.StatusKehadiran.TANPA_KETERANGAN
                elif data.status_verifikasi == dto.StatusVerifikasi.DITERIMA:
                    status_kehadiran = kehadiran.status_kehadiran
                
                kehadiran.status_kehadiran = status_kehadiran
                kehadiran.status_verifikasi = data.status_verifikasi
                kehadiran.pertemuan = pertemuan
                kehadiran.save()
                
        return Result(is_success=True, data=kehadiran_list)

class TugasService:
    def __init__(self):
        pass
    
    @staticmethod
    def hapus_tugas_dikumpul(*, user, kumpul_tugas_id: int) -> Result:
        
        kumpul_tugas = KumpulTugas.objects.filter(id=kumpul_tugas_id).first()
        if not kumpul_tugas:
            return Result(is_success=False, errors={"non_field_errors": ["Tugas tidak ditemukan"]})
        getRole = get_role(user)
        
        if getRole == "mahasiswa":

            mahasiswa = user.mahasiswa
            
            try:
                KumpulTugasRules.is_pemilik(kumpul_tugas=kumpul_tugas, mahasiswa=mahasiswa)
            except Exception as e:
                return Result(is_success=False, errors={"non_field_errors": ["Tugas bukan milik anda"]})
            
            kumpul_tugas.delete()
            return Result(is_success=True, data=kumpul_tugas, messages="Tugas berhasil dihapus")
        
        if getRole == "dosen":
            kumpul_tugas.delete()
            return Result(is_success=True, data=kumpul_tugas, messages="Tugas berhasil dihapus")
        
        return Result(is_success=False, errors={"non_field_errors": ["Tidak diizinkan untuk menghapus tugas"]})
    
    @staticmethod
    def tugas_edit(*, tugas_id, data) -> Result:
        tugas = Tugas.objects.filter(id=tugas_id).first()
        if not tugas:
            return Result(is_success=False, errors={"non_field_errors": ["Tugas tidak ditemukan"]})
        
        tugas.nama = data.nama
        tugas.url = data.url
        tugas.bobot = data.bobot
        tugas.deadline = data.deadline
        tugas.by_kehadiran = data.by_kehadiran
        tugas.save()
        return Result(is_success=True, data=tugas, messages="Tugas berhasil diubah")
    
    @staticmethod
    def kumpulan_tugas_mahasiswa(*, tugas_id:int) -> Result:
        qs = (
            KumpulTugas.objects
            .filter(tugas_id=tugas_id)
            .select_related("mahasiswa", "tugas", "nilai")
        )
        return Result(is_success=True, data=qs)
    
    @staticmethod
    def get_kumpul_tugas_by_id(*, kumpul_tugas_id:int) -> Result:
        kumpul_tugas = KumpulTugas.objects.filter(id=kumpul_tugas_id).first()
        if not kumpul_tugas:
            return Result(is_success=False, errors={"non_field_errors": ["Kumpul tugas tidak ditemukan"]})
        return Result(is_success=True, data=kumpul_tugas)

    @staticmethod
    def nilai_tugas(*, user, kumpul_tugas:int, data:dto.NilaiTugasDTO) -> Result:
        try:
            KehadiranRules.is_dosen(user)
            NilaiRules.rentang_nilai_valid(data.nilai)
            kumpul_tugas = TugasRules.kumpul_tugas_valid(kumpul_tugas)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        try:
            # update or create nilai tugas by kumpul tugas id
            nilai, created = Nilai.objects.update_or_create(
                kumpul_tugas=kumpul_tugas,
                defaults={
                    "nilai": data.nilai,
                    "catatan": data.catatan
                }
            )
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        return Result(is_success=True, data=nilai, messages="Nilai tugas berhasil disimpan")
    
    @staticmethod
    def hapus_tugas_mahasiswa(*, user, mahasiswa_id, tugas_id:int) -> Result:
        mahasiswa = Mahasiswa.objects.filter(id=mahasiswa_id).first()
        if not mahasiswa:
            return Result(is_success=False, errors={"non_field_errors": ["Mahasiswa tidak ditemukan"]})
        try:
            KehadiranRules.is_dosen(user)
            kumpul_tugas = TugasRules.mahasiswa_sudah_kumpul_tugas(tugas_id=tugas_id, mahasiswa=mahasiswa)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        kumpul_tugas.delete()
        return Result(is_success=True, messages="Tugas yang dikumpulkan berhasil dihapus")
    
    @staticmethod
    def hapus_tugas(*, user, tugas_id:int) -> Result:
        try:
            tugas = TugasRules.tugas_valid(tugas_id)
            KehadiranRules.is_dosen(user)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        tugas.delete()
        return Result(is_success=True, messages="Tugas berhasil dihapus")
    
    @staticmethod
    def kirim_tugas(*, user, tugas_id:int, pertemuan_id:int, data:dto.KirimTugasDTO) -> Result:
        try:
            KehadiranRules.is_mahasiswa(user)
            tugas = TugasRules.tugas_valid(tugas_id)
            TugasRules.sudah_deadline(tugas)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        mahasiswa = user.mahasiswa
        
        # print(mahasiswa)
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            return Result(is_success=False, errors={"non_field_errors": ["Pertemuan tidak ditemukan"]})
        
        if data.by_kehadiran and tugas.by_kehadiran:
            try:
                KehadiranRules.hadiri_pertemuan(mahasiswa=user.mahasiswa, pertemuan=pertemuan)
                kumpul_tugas = KumpulTugas.objects.create(
                    mahasiswa=mahasiswa,
                    tugas=tugas,
                    url="",
                    keterangan="by_kehadiran"
                )
                return Result(is_success=True, data=kumpul_tugas, messages="Tugas berhasil dikirim")
            except Exception as e:
                return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        try:
            kumpul_tugas = KumpulTugas.objects.create(
                mahasiswa=mahasiswa,
                tugas=tugas,
                url=data.url,
                keterangan=data.keterangan
            )
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        return Result(is_success=True, data=kumpul_tugas, messages="Tugas berhasil dikirim")
    
    @staticmethod
    def get_tugas_aktif_by_pertemuan(*, pertemuan_id:int) -> Result:
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            return Result(is_success=False, errors={"non_field_errors": ["Pertemuan tidak ditemukan"]})
        
        now = timezone.now()
        tugas = Tugas.objects.filter(pertemuan=pertemuan, deadline__gte=now)
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def get_tugas_aktif_by_mahasiswa(*, user) -> Result:
        try:
            KehadiranRules.is_mahasiswa(user)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        now = timezone.now()
        mahasiswa = user.mahasiswa
        tugas = (
            Tugas.objects
            .filter(
                deadline__gte=now,
                pertemuan__kelas__peserta__krs__mahasiswa=mahasiswa
            )
            .select_related("pertemuan__kelas__mata_kuliah", "pertemuan__kelas__peserta__krs__mahasiswa")
            .values(
                "id",
                "nama",
                "bobot",
                "url",
                "by_kehadiran",
                "pertemuan",
                "deadline",
                mata_kuliah_nama=F("pertemuan__kelas__mata_kuliah__nama"),
                mata_kuliah=F("pertemuan__kelas__mata_kuliah__id"),
                kelas=F("pertemuan__kelas__id")
            )
            .distinct()
        )
        
        # pertemuan = Pertemuan.objects.select_related(
        #     "kelas__mata_kuliah"
        # ).get(id=1)

        # print("Pertemuan:", pertemuan.id)
        # print("Kelas:", pertemuan.kelas.id)
        # print("Mata Kuliah:", pertemuan.kelas.mata_kuliah.nama)
        # print(tugas)
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def get_tugas_aktif_by_kelas(*, kelas_id:int) -> Result:
        kelas = Kelas.objects.filter(id=kelas_id).first()
        if not kelas:
            return Result(is_success=False, errors={"non_field_errors": ["Kelas tidak ditemukan"]})
        
        now = timezone.now()
        tugas = (
            Tugas.objects
            .filter(pertemuan__kelas=kelas, deadline__gte=now)
        )
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def get_tugas_by_mahasiswa(*, user) -> Result:
        try:
            KehadiranRules.is_mahasiswa(user)
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        mahasiswa = user.mahasiswa
        tugas = (
            Tugas.objects
            .filter(pertemuan__kelas__peserta__krs__mahasiswa=mahasiswa)
            .select_related("pertemuan__kelas__mata_kuliah", "pertemuan__kelas__peserta__krs__mahasiswa")
            .values(
                "id",
                "nama",
                "bobot",
                "url",
                "by_kehadiran",
                "pertemuan",
                "deadline",
                mata_kuliah_nama=F("pertemuan__kelas__mata_kuliah__nama"),
                mata_kuliah=F("pertemuan__kelas__mata_kuliah__id"),
                kelas=F("pertemuan__kelas__id"),
                kelas_nama=F("pertemuan__kelas__nama")
            )
            .distinct()
        )
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def get_tugas_by_kelas(*, kelas_id:int) -> Result:
        kelas = Kelas.objects.filter(id=kelas_id).first()
        if not kelas:
            return Result(is_success=False, errors={"non_field_errors": ["Kelas tidak ditemukan"]})
        
        # now = timezone.now()
        tugas = (
            Tugas.objects
            .filter(pertemuan__kelas=kelas)
        )
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def get_by_id(*, tugas_id:int) -> Result:
        tugas = Tugas.objects.filter(id=tugas_id).first()
        if not tugas:
            return Result(is_success=False, errors={"non_field_errors": ["Tugas tidak ditemukan"]})
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def get_tugas(*, pertemuan_id:int) -> Result:
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            return Result(is_success=False, errors={"non_field_errors": ["Pertemuan tidak ditemukan"]})
        
        tugas = Tugas.objects.filter(pertemuan=pertemuan)
        return Result(is_success=True, data=tugas)
    
    @staticmethod
    def upload_tugas(*, pertemuan_id, data: dto.UploadTugasDTO, user) -> Result:
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            return Result(is_success=False, errors={"non_field_errors": ["Pertemuan tidak ditemukan"]})
        
        try:
            KehadiranRules.is_dosen(user)
        except:
            return Result(is_success=False, errors={"non_field_errors": ["Anda tidak di izinkan"]})
        
        tugas = Tugas.objects.create(
            pertemuan=pertemuan,
            deadline=data.deadline,
            bobot=data.bobot,
            nama=data.nama,
            url=data.url,
            by_kehadiran=data.by_kehadiran
        )
        return Result(is_success=True, data=tugas, messages="Tugas berhasil diupload")

class PertemuanServices:
    def __init__(self):
        pass
    
    @staticmethod
    def pertemuan_sedang_berlangsung(*, user) -> Result:
        role = get_role(user)
        if role == "mahasiswa":
            try:
                KehadiranRules.is_mahasiswa(user)
            except:
                return Result(is_success=False, errors={"non_field_errors": ["Anda tidak di izinkan"]})
            
            now = timezone.now()
            pertemuan = (
                Pertemuan.objects
                .filter(
                    mulai__lte=now,
                    selesai__gte=now,
                    kelas__peserta__krs__mahasiswa=user.mahasiswa
                )
                .select_related("kelas__mata_kuliah")
            )
            return Result(is_success=True, data=pertemuan)
        elif role == "dosen":
            try:
                KehadiranRules.is_dosen(user)
            except:
                return Result(is_success=False, errors={"non_field_errors": ["Anda tidak di izinkan"]})
            
            now = timezone.now()
            pertemuan = (
                Pertemuan.objects
                .filter(
                    mulai__lte=now,
                    selesai__gte=now,
                    kelas__dosen=user.dosen
                )
                .select_related("kelas__mata_kuliah")
            )
            return Result(is_success=True, data=pertemuan)
        else:
            return Result(is_success=False, errors={"non_field_errors": ["User bukan mahasiswa atau dosen"]})
    
    @staticmethod
    def get_by_id(*, pertemuan_id:int) -> Result:
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            return Result(is_success=False, errors={"non_field_errors": ["Pertemuan tidak ditemukan"]})
        return Result(is_success=True, data=pertemuan)
    
    @staticmethod
    def delete_by_id(*, pertemuan_id:int) -> Result:
        pertemuan = Pertemuan.objects.filter(id=pertemuan_id).first()
        if not pertemuan:
            return Result(is_success=False, errors={"non_field_errors": ["Pertemuan tidak ditemukan"]})
        pertemuan.delete()
        return Result(is_success=True)
    
    @staticmethod
    def get_pertemuan(*, kelas_id:int) -> Result:
        kelas = (
            Kelas.objects
            .filter(id=kelas_id)
            .first()
        )
        if not kelas:
            return Result(is_success=False, message="Kelas tidak ditemukan")
        pertemuan = (
            Pertemuan.objects
            .filter(kelas=kelas)
            .select_related("kelas__mata_kuliah")
        )
        
        return Result(is_success=True, data=pertemuan)
    
    @staticmethod
    def get_pertemuan_aktif(*, kelas_id:int) -> Result:
        kelas = (
            Kelas.objects
            .filter(id=kelas_id)
            .first()
        )
        if not kelas:
            return Result(is_success=False, errors={"non_field_errors": ["Kelas tidak ditemukan"]})
        
        now = timezone.now()
        pertemuan = (
            Pertemuan.objects
            .filter(kelas=kelas, mulai__lte=now, selesai__gte=now)
            .select_related("kelas__mata_kuliah")
            # .first()
        )
        
        # if not pertemuan:
        #     return Result(is_success=True, message="Tidak ada pertemuan aktif")
        
        return Result(is_success=True, data=pertemuan)
    
    @staticmethod
    def create_pertemuan(*, kelas_id, data:dto.PertemuanDTO) -> Result:
        kelas = Kelas.objects.filter(id=kelas_id).first()
        if not kelas:
            return Result(is_success=False, message="Kelas tidak ditemukan")
        try:
            pertemuan = Pertemuan.objects.create(
                kelas=kelas,
                pertemuan_ke=data.pertemuan_ke,
                nama=data.nama,
                mulai=data.mulai,
                selesai=data.selesai
            )
        except Exception as e:
            return Result(is_success=False, errors={"non_field_errors": [str(e)]})
        
        return Result(is_success=True, data=pertemuan, messages="Pertemuan berhasil dibuat")