from .dto import AjukanBanyakKelasParamsDTO, AjukanBanyakKelasResultDTO
from academic.models import (
    Kelas,
    DetailKRS,
    PeriodeKRS,
    KRS,
    StatusKRS,
    SemesterType,
    PenawaranKRS,
    Mahasiswa,
    MataKuliah,
)
from django.db.models import Prefetch

from . import dto
from itertools import product


class Dataku:
    @staticmethod
    def mahasiswa_aktif():
        mahasiswa_qs = Mahasiswa.objects.filter(status__iexact="Aktif")
        return mahasiswa_qs

    @staticmethod
    def daftar_mata_kuliah(periode_krs_id: int):
        mata_kuliah_qs = (
            MataKuliah.objects.filter(
                kelas__isnull=False, kelas__penawarankrs__periode_krs__id=periode_krs_id
            )
            .prefetch_related(
                Prefetch(
                    "kelas_set",
                    to_attr="daftar_kelas",
                )
            )
            .distinct()
        )

        return mata_kuliah_qs

    @staticmethod
    def peserta(kelas_id: int):
        mahasiswa_qs = Mahasiswa.objects.filter(
            krs__detail__kelas__id=kelas_id
        ).distinct()
        return mahasiswa_qs

    @staticmethod
    def kelas_aktif():
        # periode_krs_aktif = PeriodeKRS.objects.filter(status__iexact="aktif").first()
        # if periode_krs_aktif:
        #     kelas_qs = Kelas.objects.filter(penawarankrs__periode_krs__id=periode_krs_aktif.id)
        kelas_qs = (
            MataKuliah.objects
            .filter(kelas__penawarankrs__periode_krs__status__iexact="aktif")
            .distinct()
            .prefetch_related(
                Prefetch(
                    "kelas_set",
                    to_attr="daftar_kelas"
                )
            )
        )
        return kelas_qs

    @staticmethod
    def mahasiswa(angkatan: int):
        prefix = str(angkatan)[-2:]

        mahasiswa_qs = Mahasiswa.objects.filter(
            nim__startswith=prefix, status__iexact="aktif"
        )
        return mahasiswa_qs


class AjukanBanyakService:
    def __init__(self):
        self.dataku = Dataku()

    def daftar_mahasiswa_aktif(self):
        hasil = self.dataku.mahasiswa_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_kelas_aktif(self):
        hasil = self.dataku.kelas_aktif()
        return dto.Result(is_success=True, data=hasil)

    def daftar_mahasiswa(self, angkatan: int) -> dto.Result:
        hasil = self.dataku.mahasiswa(angkatan)
        return dto.Result(is_success=True, data=hasil)

    def daftar_peserta(self, kelas_id: int) -> dto.Result:
        hasil = self.dataku.peserta(kelas_id)
        return dto.Result(is_success=True, data=hasil)

    def daftar_mata_kuliah(self, periode_krs_id: int = 1) -> dto.Result:
        hasil = self.dataku.daftar_mata_kuliah(periode_krs_id)
        return dto.Result(is_success=True, data=hasil)

    def buat_krs(self, mahasiswa_ids: list[int]) -> bool:
        periode_krs_aktif = PeriodeKRS.objects.filter(status="aktif").first()
        if periode_krs_aktif is None:
            return False

        # ----- buat banyak krs untuk id yang belum buat -----
        krs_list = [
            KRS(
                mahasiswa_id=mahasiswa_id,
                semester=periode_krs_aktif.semester,
                tahun_ajaran=periode_krs_aktif.tahun_ajaran,
            )
            for mahasiswa_id in mahasiswa_ids
        ]

        KRS.objects.bulk_create(
            krs_list,
            ignore_conflicts=True,
        )

        return True

    def ajukan_banyak(
        self, params: AjukanBanyakKelasParamsDTO
    ) -> AjukanBanyakKelasResultDTO:

        # ----- aturan: harus ada krs aktif -----
        periode_krs_aktif = PeriodeKRS.objects.filter(status="aktif").first()
        if periode_krs_aktif is None:
            return AjukanBanyakKelasResultDTO(
                is_success=False,
                errors={"non_field_errors": ["Periode KRS belum diatur"]},
            )

        # ----- aturan: tidak boleh mahasiswa_ids atau kelas_ids kosong -----
        if len(params.kelas_ids) == 0 or len(params.mahasiswa_ids) == 0:
            return AjukanBanyakKelasResultDTO(
                is_success=False,
                errors={
                    "non_field_errors": ["Kelas atau mahasiswa tidak boleh kosong"]
                },
            )

        # ----- validasi id mahasiswa -----
        for mahasiswa_id in params.mahasiswa_ids:
            if not Mahasiswa.objects.filter(id=mahasiswa_id).exists():
                return AjukanBanyakKelasResultDTO(
                    is_success=False,
                    errors={"non_field_errors": ["Mahasiswa tidak ditemukan"]},
                )

        # ----- validasi id kelas -----
        for kelas_id in params.kelas_ids:
            if not Kelas.objects.filter(id=kelas_id).exists():
                return AjukanBanyakKelasResultDTO(
                    is_success=False,
                    errors={"non_field_errors": ["Kelas tidak ditemukan"]},
                )

        # ----- mahaiswa buat krs bagi yang belum buat -----
        is_valid = self.buat_krs(params.mahasiswa_ids)
        if not is_valid:
            return AjukanBanyakKelasResultDTO(
                is_success=False,
                errors={
                    "non_field_errors": ["terdapat mahasiswa yang belum membuat krs"]
                },
            )

        mahasiswa_ids = params.mahasiswa_ids
        mahasiswa_ids = [161, 95]
        # print(len(mahasiswa_ids))
        kelas_ids = params.kelas_ids
        kelas_ids = [170, 169, 168]

        # ----- aturan: semua mahasiswa telah membuat krs -----
        krs_qs = KRS.objects.filter(
            mahasiswa_id__in=mahasiswa_ids,
            semester=periode_krs_aktif.semester,
            tahun_ajaran=periode_krs_aktif.tahun_ajaran,
        )
        if len(krs_qs) != len(mahasiswa_ids):
            return AjukanBanyakKelasResultDTO(
                is_success=False,
                errors={
                    "non_field_errors": ["terdapat mahasiswa yang belum membuat krs"]
                },
            )

        # create krs
        krs_qs = KRS.objects.filter(
            mahasiswa_id__in=mahasiswa_ids,
            semester=periode_krs_aktif.semester,
            tahun_ajaran=periode_krs_aktif.tahun_ajaran,
        )

        kelas_qs = Kelas.objects.filter(id__in=kelas_ids)

        # ----- aturan: kelas_qs dan krs_qs tidak boleh kosong -----
        if len(kelas_qs) == 0 or len(krs_qs) == 0:
            return AjukanBanyakKelasResultDTO(
                is_success=False,
                errors={"non_field_errors": ["Kelas atau krs tidak boleh kosong"]},
            )

        # ----- aturan: semua kelas harus terdaftar dalam penawaranKRS -----
        penawaran_krs = PenawaranKRS.objects.filter(
            periode_krs=periode_krs_aktif,
            kelas__in=kelas_qs,
        )
        if len(penawaran_krs) != len(kelas_qs):
            return AjukanBanyakKelasResultDTO(
                is_success=False,
                errors={
                    "non_field_errors": [
                        "Semua kelas harus terdaftar dalam penawaranKRS"
                    ]
                },
            )

        # print(kelas_qs)

        # print(krs_qs)
        # print("len: krs_qs", len(krs_qs))

        # create detail krs
        detail_krs_list = [
            DetailKRS(krs=krs_id, kelas=kelas_id)
            for krs_id, kelas_id, in product(krs_qs, kelas_qs)
        ]
        # DetailKRS.objects.bulk_create(detail_krs_list, ignore_conflicts=True)
        print(detail_krs_list)

        return AjukanBanyakKelasResultDTO(
            is_success=True,
            message="berhasil mengajukan banyak kelas",
            data=detail_krs_list,
        )

    def daftar_krs(self):
        periode_krs_aktif = PeriodeKRS.objects.filter(status="aktif").first()
        if periode_krs_aktif is None:
            raise Exception("Periode KRS belum diatur")

        krs_qs = KRS.objects.filter(
            semester=periode_krs_aktif.semester,
            tahun_ajaran=periode_krs_aktif.tahun_ajaran,
        )
