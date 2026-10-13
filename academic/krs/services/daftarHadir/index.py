from itertools import product

from django.db.models import Prefetch, Q
from django.db import transaction
from django.core.exceptions import ValidationError

from academic.models import (
    KRS,
    DetailKRS,
    PeriodeKRS,
    Mahasiswa,
    Kelas,
    MataKuliah,
    PenawaranKRS,
)

from . import serializers, dto

class Command:

    @staticmethod
    @transaction.atomic
    def tambah_kelas(*, mata_kuliah_id: int, nama_kelas: str, kuota: int = 60):
        mata_kuliah = MataKuliah.objects.get(id=mata_kuliah_id)

        periode_krs = PeriodeKRS.objects.filter(status__iexact="aktif").first()

        if periode_krs is None:
            raise ValueError("Tidak ada periode KRS aktif.")

        kelas = Kelas.objects.create(
            mata_kuliah=mata_kuliah,
            nama=nama_kelas,
        )

        penawaran_krs = PenawaranKRS.objects.create(
            periode_krs=periode_krs,
            kelas=kelas,
            kuota=kuota,
        )

        return penawaran_krs

    @staticmethod
    def hapus_kelas(*, kelas_id: int):
        Kelas.objects.filter(id=kelas_id).delete()
        return True

    @staticmethod
    def ganti_nama(*, kelas_id: int, nama_kelas: str):
        Kelas.objects.filter(id=kelas_id).update(nama=nama_kelas)
        return True

    @staticmethod
    def get_periode_krs():
        periode_krs = PeriodeKRS.objects.filter(status__iexact="aktif").first()
        if periode_krs is None:
            raise ValueError("Tidak ada periode KRS aktif.")
        return periode_krs

    @staticmethod
    @transaction.atomic
    def tambah_peserta(
        *,
        kelas_id: int,
        mahasiswa_ids: list[int],
    ):
        kelas = Kelas.objects.get(id=kelas_id)

        # penawaran_krs = PenawaranKRS.objects.select_related("periode_krs").get(kelas=kelas)

        periode_krs = Command.get_periode_krs()

        krs_list = KRS.objects.filter(
            mahasiswa_id__in=mahasiswa_ids,
            semester=periode_krs.semester,
            tahun_ajaran=periode_krs.tahun_ajaran,
        )

        detail_list = [
            DetailKRS(
                krs=krs,
                kelas=kelas,
            )
            for krs in krs_list
        ]

        DetailKRS.objects.bulk_create(
            detail_list,
            ignore_conflicts=True,
        )

        return len(detail_list)


    @staticmethod
    @transaction.atomic
    def hapus_peserta(
        *,
        kelas_id: int,
        mahasiswa_ids: list[int],
    ):
        jumlah_dihapus, _ = DetailKRS.objects.filter(
            kelas_id=kelas_id,
            krs__mahasiswa_id__in=mahasiswa_ids,
        ).delete()

        return jumlah_dihapus
    
    @staticmethod
    @transaction.atomic
    def gabung_banyak_kelas(
        *,
        kelas_ids: list[int],
        mahasiswa_ids: list[int],
    ) -> int:
        periode_krs = Command.get_periode_krs()
        krs_list = KRS.objects.filter(
            mahasiswa_id__in=mahasiswa_ids,
            semester=periode_krs.semester,
            tahun_ajaran=periode_krs.tahun_ajaran,
        )
        
        # hapus dulu semua detail krs yang ada
        DetailKRS.objects.filter(
            krs__mahasiswa_id__in=mahasiswa_ids,
        ).delete()

        # detail_list = [
        #     DetailKRS(krs=krs, kelas_id=kelas_id)
        #     for krs in krs_list
        #     for kelas_id in kelas_ids
        # ]
        
        detail_list = [
            DetailKRS(krs=krs, kelas_id=kelas_id)
            for krs, kelas_id in product(krs_list, kelas_ids)
        ]

        DetailKRS.objects.bulk_create(
            detail_list,
            ignore_conflicts=True,
        )

        return len(detail_list)
    

    @staticmethod
    @transaction.atomic
    def tambah_banyak_peserta(
        *,
        kelas_ids: list[int],
        mahasiswa_ids: list[int],
    ) -> int:
        if not kelas_ids or not mahasiswa_ids:
            raise ValidationError(
                "Kelas dan mahasiswa harus diisi."
            )

        kelas_ids = list(set(kelas_ids))
        mahasiswa_ids = list(set(mahasiswa_ids))
        
        periode_krs = Command.get_periode_krs()

        # Ambil penawaran kelas pada periode aktif
        penawaran_list = list(
            PenawaranKRS.objects.filter(
                kelas_id__in=kelas_ids,
                periode_krs=periode_krs,
            ).select_related(
                "kelas__mata_kuliah",
                "periode_krs",
            )
        )

        penawaran_by_kelas = {
            penawaran.kelas_id: penawaran
            for penawaran in penawaran_list
        }

        if len(penawaran_by_kelas) != len(kelas_ids):
            raise ValidationError(
                "Sebagian kelas tidak memiliki penawaran "
                "pada periode KRS aktif."
            )

        periode_ids = {
            penawaran.periode_krs_id
            for penawaran in penawaran_list
        }

        if len(periode_ids) != 1:
            raise ValidationError(
                "Semua kelas harus berasal dari periode KRS yang sama."
            )

        periode_krs = penawaran_list[0].periode_krs

        # Ambil KRS mahasiswa pada semester dan tahun ajaran terkait
        krs_list = list(
            KRS.objects.filter(
                mahasiswa_id__in=mahasiswa_ids,
                semester=periode_krs.semester,
                tahun_ajaran=periode_krs.tahun_ajaran,
            ).select_related("mahasiswa")
        )

        krs_by_mahasiswa = {
            krs.mahasiswa_id: krs
            for krs in krs_list
        }

        mahasiswa_tidak_punya_krs = (
            set(mahasiswa_ids) - set(krs_by_mahasiswa)
        )

        if mahasiswa_tidak_punya_krs:
            raise ValidationError(
                "Sebagian mahasiswa belum memiliki KRS "
                "pada periode tersebut: "
                f"{sorted(mahasiswa_tidak_punya_krs)}"
            )

        # Cegah memilih beberapa kelas dari mata kuliah yang sama
        mata_kuliah_ids = [
            penawaran.kelas.mata_kuliah_id
            for penawaran in penawaran_list
        ]

        if len(mata_kuliah_ids) != len(set(mata_kuliah_ids)):
            raise ValidationError(
                "Terdapat beberapa kelas dari mata kuliah yang sama."
            )

        detail_baru = []

        for krs in krs_list:
            detail_lama = list(
                DetailKRS.objects.filter(
                    krs=krs
                ).select_related(
                    "kelas__mata_kuliah"
                )
            )

            # Hitung SKS berdasarkan mata kuliah unik
            sks_lama = {
                detail.kelas.mata_kuliah_id:
                    detail.kelas.mata_kuliah.sks
                for detail in detail_lama
            }

            kelas_lama = {
                detail.kelas_id
                for detail in detail_lama
            }

            mata_kuliah_lama = set(sks_lama)

            # Hindari menambahkan mata kuliah yang sudah diambil
            mata_kuliah_baru = {
                penawaran.kelas.mata_kuliah_id:
                    penawaran.kelas.mata_kuliah.sks
                for penawaran in penawaran_list
                if penawaran.kelas_id not in kelas_lama
            }

            duplikat_mk = (
                mata_kuliah_lama & set(mata_kuliah_baru)
            )

            if duplikat_mk:
                raise ValidationError(
                    f"Mahasiswa {krs.mahasiswa_id} sudah mengambil "
                    f"mata kuliah ID {sorted(duplikat_mk)}."
                )

            total_sks = (
                sum(sks_lama.values())
                + sum(mata_kuliah_baru.values())
            )

            if total_sks > 24:
                raise ValidationError(
                    f"Mahasiswa {krs.mahasiswa_id}: total SKS "
                    f"akan menjadi {total_sks}, melebihi batas 24 SKS."
                )

            for penawaran in penawaran_list:
                if penawaran.kelas_id not in kelas_lama:
                    detail_baru.append(
                        DetailKRS(
                            krs=krs,
                            kelas_id=penawaran.kelas_id,
                        )
                    )

        DetailKRS.objects.bulk_create(
            detail_baru,
            ignore_conflicts=True,
        )

        return len(detail_baru)


class Dataku:
    @staticmethod
    def mata_kuliah_kelas(periode_krs: PeriodeKRS):
        kelas_qs = (
            MataKuliah.objects.filter(
                kelas__penawarankrs__periode_krs=periode_krs,
                kelas__peserta__krs__semester=periode_krs.semester,
                kelas__peserta__krs__tahun_ajaran=periode_krs.tahun_ajaran,
            )
            .distinct()
            .prefetch_related(Prefetch("kelas_set", to_attr="daftar_kelas"))
        )
        return kelas_qs
    
    @staticmethod
    def penawaran_mata_kuliah_kelas(periode_krs: PeriodeKRS):
        kelas_qs = (
            MataKuliah.objects.filter(
                kelas__penawarankrs__periode_krs=periode_krs,
                # kelas__peserta__krs__semester=periode_krs.semester,
                # kelas__peserta__krs__tahun_ajaran=periode_krs.tahun_ajaran,
            )
            .distinct()
            .prefetch_related(Prefetch("kelas_set", to_attr="daftar_kelas"))
        )
        return kelas_qs

    @staticmethod
    def detailKRS(*, krs: KRS):
        detail_krs_qs = DetailKRS.objects.filter(krs=krs).select_related(
            "kelas", "kelas__mata_kuliah"
        )
        return detail_krs_qs

    @staticmethod
    def mahasiswa(periode_krs: PeriodeKRS):
        mahasiswa_qs = Mahasiswa.objects.filter(
            krs__semester=periode_krs.semester,
            krs__tahun_ajaran=periode_krs.tahun_ajaran,
            status__iexact="aktif",
        )
        return mahasiswa_qs

    @staticmethod
    def krs(periode_krs: PeriodeKRS):
        krs_qs = KRS.objects.filter(
            semester=periode_krs.semester, tahun_ajaran=periode_krs.tahun_ajaran
        ).select_related("mahasiswa")
        return krs_qs

    @staticmethod
    def detail_krs_all(periode_krs: PeriodeKRS):

        detail_krs_qs = DetailKRS.objects.filter(
            krs__semester=periode_krs.semester,
            krs__tahun_ajaran=periode_krs.tahun_ajaran,
        ).select_related(
            "krs__mahasiswa",
        )

        return detail_krs_qs

    @staticmethod
    def daftar_krs_by_kelas(*, kelas_id: int, periode_krs: PeriodeKRS):
        hasil_qs = KRS.objects.filter(
            semester=periode_krs.semester,
            tahun_ajaran=periode_krs.tahun_ajaran,
            detail__kelas__id=kelas_id,
        ).select_related("mahasiswa")

        return hasil_qs


class KelaService:
    def __init__(self):
        self.cmd = Command
        
    def tambah_kelas(self, *, mata_kuliah_id: int, nama_kelas: str, kuota: int = 60) -> dto.Result:
        self.cmd.tambah_kelas(mata_kuliah_id=mata_kuliah_id, nama_kelas=nama_kelas, kuota=kuota)
        return dto.Result(is_success=True, data={"message": "Kelas berhasil ditambahkan."})
    
    def hapus_kelas(self, *, kelas_id: int) -> dto.Result:
        self.cmd.hapus_kelas(kelas_id=kelas_id)
        return dto.Result(is_success=True, data={"message": "Kelas berhasil dihapus."})
    
    def ganti_nama(self, *, kelas_id: int, nama_kelas: str) -> dto.Result:
        self.cmd.ganti_nama(kelas_id=kelas_id, nama_kelas=nama_kelas)
        return dto.Result(is_success=True, data={"message": "Kelas berhasil diubah."})
        
    def gabung_banyak_kelas(self, *, kelas_ids: list[int], mahasiswa_ids: list[int]) -> dto.Result:
        result = self.cmd.gabung_banyak_kelas(
            kelas_ids=kelas_ids,
            mahasiswa_ids=mahasiswa_ids,
        )
        if result > 0:
            return dto.Result(is_success=True)
        else:
            return dto.Result(is_success=False)
        
    def tambah_banyak_peserta(self, kelas_ids: list[int], mahasiswa_ids: list[int]) -> dto.Result:
        result = self.cmd.gabung_banyak_kelas(
            kelas_ids=kelas_ids,
            mahasiswa_ids=mahasiswa_ids,
        )
        if result > 0:
            return dto.Result(is_success=True, data=result)
        else:
            return dto.Result(is_success=False)
        
        
    def daftar_peserta(self, kelas_id: int) -> dto.Result:
        hasil = self.dataku.daftar_krs_by_kelas(kelas_id=kelas_id)
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_mahasiswa(self, angkatan: int) -> dto.Result:
        hasil = self.dataku.mahasiswa(angkatan=angkatan)
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_mata_kuliah(self, periode_krs_id: int = 1) -> dto.Result:
        hasil = self.dataku.mata_kuliah_kelas(periode_krs_id=periode_krs_id)
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_kelas_aktif(self) -> dto.Result:
        hasil = self.dataku.kelas_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_mahasiswa_aktif(self) -> dto.Result:
        hasil = self.dataku.mahasiswa_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_peserta_aktif(self) -> dto.Result:
        hasil = self.dataku.peserta_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_mata_kuliah_aktif(self) -> dto.Result:
        hasil = self.dataku.mata_kuliah_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_krs_aktif(self) -> dto.Result:
        hasil = self.dataku.krs_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_detail_krs_aktif(self) -> dto.Result:
        hasil = self.dataku.detail_krs_aktif()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_detail_krs_all(self) -> dto.Result:
        hasil = self.dataku.detail_krs_all()
        return dto.Result(is_success=True, data=hasil)
    
    def daftar_krs_by_kelas(self, kelas_id: int) -> dto.Result:
        hasil = self.dataku.daftar_krs_by_kelas(kelas_id=kelas_id)
        return dto.Result(is_success=True, data=hasil)

class LihatDaftarKRS:
    def __init__(self):
        self.dataku = Dataku

    def peserta_kelas(self, kelas_id: int):
        periode_krs = self.periode_krs
        peserta_qs = self.dataku.daftar_krs_by_kelas(
            kelas_id=kelas_id, periode_krs=periode_krs
        )
        return dto.Result(is_success=True, data=peserta_qs)

    @property
    def mata_kuliah_kelas(self):
        periode_krs = self.periode_krs
        mata_kuliah_qs = self.dataku.mata_kuliah_kelas(periode_krs)
        return dto.Result(is_success=True, data=mata_kuliah_qs)
    
    @property
    def penawaran_mata_kuliah_kelas(self):
        periode_krs = self.periode_krs
        mata_kuliah_qs = self.dataku.penawaran_mata_kuliah_kelas(periode_krs)
        return dto.Result(is_success=True, data=mata_kuliah_qs)

    @property
    def krs(self):
        periode_krs = self.periode_krs
        krs_qs = self.dataku.krs(periode_krs)
        return dto.Result(is_success=True, data=krs_qs)
        # serializer = serializers.KRSSerializer(krs_qs, many=True)
        # return serializer.data

    def detail_krs(self, krs_id: int):
        krs = KRS.objects.filter(id=krs_id).first()
        detail_krs_qs = self.dataku.detailKRS(krs=krs)
        return dto.Result(is_success=True, data=detail_krs_qs)
        # serializer = serializers.DetailKRSSerializer(detail_krs_qs, many=True)
        # return serializer.data

    @property
    def mahasiswa(self) -> dto.Result:
        periode_krs = self.periode_krs
        mahasiswa_qs = self.dataku.mahasiswa(periode_krs)
        return dto.Result(is_success=True, data=mahasiswa_qs)
        # serializer = serializers.MahasiswaSerializer(mahasiswa_qs, many=True)
        # return serializer.data

    @property
    def periode_krs(self):
        hasil = PeriodeKRS.objects.filter(status__iexact="aktif").first()
        if hasil is None:
            raise Exception("Periode KRS belum diatur")
        return hasil

    def lihat_daftar_krs(self):
        periode_krs = self.periode_krs
        detail_krs_qs = self.dataku.detail_krs_all(periode_krs)
        serializer = serializers.DetailKRSSerializer(detail_krs_qs, many=True)
        return serializer.data
