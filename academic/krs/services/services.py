from django.db import transaction
from ..dto import mhs_dto
from ..dto import dto

# ----- service -----
from accounts.mahasiswa.services import MahasiswaService

# from .validasiKRS import ValidasiKRS

# ----- rules -----
from ..rules.rules import KRSRules

from academic.models import KRS, DetailKRS, Kelas, PenawaranKRS, PeriodeKRS, StatusKRS
from django.db.models import Q


class Core:
    @staticmethod
    def penawaran_krs(periode_id, semester_level=0) -> dto.Result:
        periode_krs = PeriodeKRS.objects.filter(id=periode_id).first()
        if periode_krs is None:
            return dto.Result(
                is_success=False, errors={"periode_id": ["Periode KRS tidak ditemukan"]}
            )

        penawaran_krs_qs = (
            PenawaranKRS.objects.select_related(
                "periode_krs",
                "kelas",
                "kelas__mata_kuliah",
            )
            .filter(periode_krs=periode_krs)
            .order_by(
                "kelas__mata_kuliah__semester",
                "kelas__mata_kuliah__nama",
            )
        )

        if semester_level != 0:
            penawaran_krs_qs = penawaran_krs_qs.filter(
                kelas__mata_kuliah__semester=semester_level
            )

        return dto.Result(is_success=True, data=penawaran_krs_qs)

    @staticmethod
    def krs_kelas_pasarwajo(periode_id) -> dto.Result:
        periode_krs_aktif = PeriodeKRS.objects.filter(id=periode_id).first()
        if not periode_krs_aktif:
            return dto.Result(
                is_success=False,
                errors={"non_field_errors": ["Periode KRS belum diatur"]},
            )

        penawaran = (
            PenawaranKRS.objects.filter(periode_krs_id=periode_krs_aktif.id)
            .select_related(
                "kelas",
                "kelas__mata_kuliah",
            )
            .prefetch_related("kelas__peserta__krs__mahasiswa")
        )

        hasil = {}
        for item in penawaran:
            mata_kuliah = item.kelas.mata_kuliah

            if mata_kuliah.id not in hasil:
                hasil[mata_kuliah.id] = {
                    "id": mata_kuliah.id,
                    "kode": mata_kuliah.kode,
                    "nama": mata_kuliah.nama,
                    "kelas": [],
                }

            hasil[mata_kuliah.id]["kelas"].append(
                {
                    "id": item.kelas.id,
                    "nama": item.kelas.nama,
                    "mahasiswa": [
                        {
                            "id": detail.krs.mahasiswa.id,
                            "nim": detail.krs.mahasiswa.nim,
                            "nama": detail.krs.mahasiswa.nama,
                        }
                        for detail in item.kelas.peserta.all()
                    ],
                }
            )
            
        return dto.Result(is_success=True, data=hasil)

    @staticmethod
    def periode_krs_aktif() -> dto.Result:
        periode_krs = PeriodeKRS.objects.filter(status="aktif").first()
        if periode_krs is None:
            return dto.Result(
                is_success=False,
                errors={"non_field_errors": ["Periode KRS belum diatur"]},
            )
        return dto.Result(is_success=True, data=periode_krs)

    @staticmethod
    def kelas_aktif(periode_id) -> dto.Result:
        periode_krs = PeriodeKRS.objects.filter(id=periode_id).first()
        if periode_krs is None:
            return dto.Result(
                is_success=False,
                errors={"non_field_errors": ["Periode KRS belum diatur"]},
            )

        kelas_list = Kelas.objects.select_related("mata_kuliah").filter(
            penawarankrs__periode_krs=periode_krs
        )
        return dto.Result(is_success=True, data=kelas_list)

    @staticmethod
    def hitung_total_sks(krs_id) -> int:
        krs = KRS.objects.filter(id=krs_id).first()
        if not krs:
            return 0
        sks_list = DetailKRS.objects.filter(krs=krs).values_list(
            "kelas__mata_kuliah__sks", flat=True
        )
        hasil = sum(sks_list)
        return hasil

    @staticmethod
    def generate_banyak_krs(data: dto.GenerateBanyakKRSRequest) -> dto.Result:

        try:
            with transaction.atomic():

                mahasiswa_list = MahasiswaService.get_all_by_nim(data.daftar_nim)

                krs_list = [
                    KRS(
                        mahasiswa=mahasiswa,
                        semester=data.semester,
                        tahun_ajaran=data.tahun_ajaran,
                    )
                    for mahasiswa in mahasiswa_list
                ]

                KRS.objects.bulk_create(krs_list)

            return dto.Result(is_success=True)

        except Exception as e:
            return dto.Result(is_success=False, errors={"non_field_error": [str(e)]})


class Mhs:
    def __init__(self):
        pass

    @staticmethod
    def krs_saya(*, nim, tahun_ajaran: str, semester_type: str) -> dto.Result:
        krs = krs = KRS.objects.filter(
            tahun_ajaran=tahun_ajaran, semester=semester_type, mahasiswa__nim=nim
        ).first()
        if krs is None:
            return dto.Result(
                is_success=False, errors={"krs_id": ["KRS tidak ditemukan"]}
            )

        kelas_dipilih_ids = DetailKRS.objects.filter(krs=krs).values_list(
            "kelas_id", flat=True
        )

        return dto.Result(is_success=True, data=kelas_dipilih_ids)

    @staticmethod
    def krs_mahasiswa(krs_id, tahun_ajaran: str, semester_type: str) -> dto.Result:
        krs = KRS.objects.filter(
            id=krs_id, tahun_ajaran=tahun_ajaran, semester=semester_type
        ).first()
        if krs is None:
            return dto.Result(
                is_success=False, errors={"krs_id": ["KRS tidak ditemukan"]}
            )

        return dto.Result(is_success=True, data=krs)

    def buat_krs(self, data: mhs_dto.BuatKrs) -> dto.Result:
        mahasiswa = MahasiswaService.get_by_nim(data.nim)

        if mahasiswa is None:
            return dto.Result(is_success=False, errors={"nim": ["nim tidak ditemukan"]})

        # jika sudah ada
        if KRS.objects.filter(
            mahasiswa=mahasiswa, tahun_ajaran=data.tahun_ajaran, semester=data.semester
        ).exists():
            return dto.Result(is_success=False, errors={"nim": ["KRS sudah ada"]})

        # buat krs baru
        krs = KRS.objects.create(
            mahasiswa=mahasiswa,
            semester=data.semester,
            tahun_ajaran=data.tahun_ajaran,
            status=StatusKRS.DRAFT,
        )
        return dto.Result(is_success=True)

    def buat_atau_update(self, data: mhs_dto.BuatKrs) -> dto.Result:
        mahasiswa = MahasiswaService.get_by_nim(data.nim)

        if mahasiswa is None:
            return dto.Result(is_success=False, errors={"nim": ["nim tidak ditemukan"]})

        # jika sudah ada
        if KRS.objects.filter(
            mahasiswa=mahasiswa, tahun_ajaran=data.tahun_ajaran, semester=data.semester
        ).exists():
            krs = KRS.objects.filter(
                mahasiswa=mahasiswa,
                tahun_ajaran=data.tahun_ajaran,
                semester=data.semester,
            ).first()
            return dto.Result(is_success=True, data=krs.id)

        # buat krs baru
        krs = KRS.objects.create(
            mahasiswa=mahasiswa,
            semester=data.semester,
            tahun_ajaran=data.tahun_ajaran,
            status=StatusKRS.DRAFT,
        )
        return dto.Result(is_success=True, data=krs.id)

    @staticmethod
    def tambah_banyak_kelas(data: mhs_dto.TambahBanyakKelas, user=None) -> dto.Result:
        if len(data.kelas_ids) == 0:
            return dto.Result(
                is_success=False, errors={"kelas_ids": ["Kelas tidak boleh kosong"]}
            )

        krs = KRS.objects.filter(id=data.krs_id).first()
        if not krs:
            return dto.Result(
                is_success=False, errors={"krs_id": ["KRS tidak ditemukan"]}
            )

        # terapkan aturan krs
        try:
            KRSRules.ensure_owner(krs, user.mahasiswa.id)
            KRSRules.ensure_can_submit(krs)
        except Exception as e:
            return dto.Result(is_success=False, errors={e.field: [e.message]})

        detail_krs_list = []
        for kelas_id in data.kelas_ids:
            kelas = Kelas.objects.filter(id=kelas_id).first()
            if not kelas:
                return dto.Result(
                    is_success=False, errors={"kelas_id": ["Kelas tidak ditemukan"]}
                )

            detail_krs_list.append(DetailKRS(krs=krs, kelas=kelas))

        # jumlah kan dulu semua apakah lebih dari 24 sks
        total_sks = 0
        for detail_krs in detail_krs_list:
            total_sks += detail_krs.kelas.mata_kuliah.sks

        if total_sks > 24:
            return dto.Result(
                is_success=False,
                errors={"non_field_errors": ["Jumlah SKS melebihi batas"]},
            )

        with transaction.atomic():
            # hapus semua item yang ada di krs
            DetailKRS.objects.filter(krs=krs).delete()

            DetailKRS.objects.bulk_create(detail_krs_list)

            # update krs
            krs.status = StatusKRS.DRAFT
            krs.save()
            return dto.Result(is_success=True)

        return dto.Result(
            is_success=False, errors={"non_field_errors": ["Terjadi kesalahan"]}
        )

    def tambah_kelas(self, data: mhs_dto.TambahKelas) -> dto.Result:

        # validasi apakah krs tersedia
        krs = KRS.objects.filter(id=data.krs_id).first()
        if krs is None:
            return dto.Result(
                is_success=False, errors={"krs_id": ["KRS tidak ditemukan"]}
            )

        # validasi apakah kelas tersedia
        kelas = Kelas.objects.filter(id=data.kelas_id).first()
        if kelas is None:
            return dto.Result(
                is_success=False, errors={"kelas_id": ["Kelas tidak ditemukan"]}
            )

        # validasi apakah kelas sudah ada di krs
        if DetailKRS.objects.filter(krs=krs, kelas=kelas).exists():
            return dto.Result(
                is_success=False, errors={"kelas_id": ["Kelas sudah ada di KRS"]}
            )

        DetailKRS.objects.create(krs=krs, kelas=kelas)
        return dto.Result(is_success=True)

    def hapus_kelas(self):
        pass

    def simpan_draft(self):
        pass

    @staticmethod
    def ajukan_krs(krs_id, mahasiswa_id=None) -> dto.Result:
        krs = KRS.objects.filter(id=krs_id).first()
        if not krs:
            return dto.Result(
                is_success=False, errors={"non_field_errors": ["krs tidak ditemukan"]}
            )

        if mahasiswa_id:
            if krs.mahasiswa.id != mahasiswa_id:
                return dto.Result(
                    is_success=False,
                    errors={"non_field_errors": ["ini bukan krs anda"]},
                )

        krs.status = StatusKRS.DIAJUKAN
        krs.save()
        return dto.Result(is_success=True)

    def lihat_status_pengajuan(self):
        pass

    def perbaiki_krs(self):
        pass

    def cetak_krs(self):
        pass


class DosenPA:
    def __init__(self):
        pass

    def lihat_pengajuan_krs(self):
        pass

    @staticmethod
    def detail_krs_mahasiswa(krs_id) -> dto.Result:
        krs = KRS.objects.filter(id=krs_id).first()
        if krs is None:
            return dto.Result(
                is_success=False, errors={"krs_id": ["KRS tidak ditemukan"]}
            )

        list_obj = DetailKRS.objects.filter(krs=krs)
        # if not list_obj:
        #     return dto.Result(is_success=False, errors={"krs_id": ["KRS tidak ditemukan"]})

        return dto.Result(is_success=True, data=list_obj)

    def lihat_detail_krs_mahasiswa(self):
        pass

    def setujui_krs(self):
        pass

    def tolak_krs(self):
        pass

    def minta_perbaiki(self):
        pass


class TU:
    def __init__(self):
        pass

    def lihat_krs(self):
        pass
