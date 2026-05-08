from academic.services import (
    DetailKRSService,
    KelasService,
    KRSService,
    MataKuliahService,
)

from accounts.services import (
    MahasiswaService
)

from academic.helpers.helpers import (
    validate_form_data
)

from django.db import transaction

class IsiKRS:
    """
    Menyimpan KRS sealigu
    
    Args:
        KRSService, MahasiswaService, MataKuliahService, KelasService        
    """
    def __init__(
        self, krs_service: KRSService,
        mahasiswa_service: MahasiswaService,
        mata_kuliah_service: MataKuliahService,
        kelas_service: KelasService,
        detail_krs_service: DetailKRSService
    ):
        self.krs_service = krs_service
        self.mahasiswa_service = mahasiswa_service
        self.mata_kuliah_service = mata_kuliah_service
        self.kelas_service = kelas_service
        self.detail_krs_service = detail_krs_service
        
    def _validate_form_data(self, form_data):
        return validate_form_data(form_data)
        
    @transaction.atomic
    def execute(self, form_data):
        """
        Mengisi KRS banyak mahasiswa sekaligus
        akan side effect pada database krs dan detail krs
        
        Args:
            form_data (dict): data yang diambil dari form
            
                {
                    "tahun_ajaran": "2025/2026",
                    "semester": "genap" or "ganjil",
                    "daftar_nim": ["22650151", "22650152", "22650153", "22650154", "22650155"],
                    "daftar_kode_mata_kuliah": [1, 2, 3, 4]
                }
            
        Returns:
            None
        
        Raises:

            ValueError: jika ada kelas yang bentrok
            
        Example:
            >>> execute(form_data)
        """
        
        # validasi data
        errors = self._validate_form_data(form_data)
        if errors:
            raise ValueError(errors)
        
        
        
        # 1. Ambil semua data referensi dulu

        mahasiswa_map = {
            m.nim: m
            for m in self.mahasiswa_service.model.objects.filter(nim__in=form_data["daftar_nim"])
        }

        matkul_map = {
            mk.kode: mk
            for mk in self.mata_kuliah_service.model.objects.filter(kode__in=form_data["daftar_kode_mata_kuliah"])
        }
        
        # 2. Ambil kelas berdasarkan matakuliah
        kelas_qs = self.kelas_service.model.objects.filter(mata_kuliah__kode__in=form_data["daftar_kode_mata_kuliah"])

        kelas_map = {}
        for k in kelas_qs:
            kelas_map.setdefault(k.mata_kuliah.kode, []).append(k)
            
        # 3. Buat / ambil KRS (per mahasiswa)
        existing_krs = self.krs_service.model.objects.filter(mahasiswa__nim__in=form_data["daftar_nim"])
        krs_map = {
            k.mahasiswa.nim: k
            for k in existing_krs
        }
        
        # buat yang belum ada
        new_krs = []
        for nim in form_data["daftar_nim"]:
            if nim not in krs_map:
                new_krs.append(self.krs_service.model(mahasiswa=mahasiswa_map[nim], tahun_ajaran=form_data["tahun_ajaran"], semester=form_data["semester"]))
        self.krs_service.model.objects.bulk_create(new_krs) # side effect

        # refresh map
        for k in self.krs_service.model.objects.filter(mahasiswa__nim__in=form_data["daftar_nim"]):
            krs_map[k.mahasiswa.nim] = k
            
            
        # 4 Siapkan DetailKRS (inti proses)

        detail_objs = []

        for nim in form_data["daftar_nim"]:
            krs = krs_map[nim]

            for kode in list(matkul_map.keys()):
                kelas_list = kelas_map.get(kode, [])

                for kelas in kelas_list:
                    detail_objs.append(
                        self.detail_krs_service.model(
                            krs=krs,
                            kelas=kelas
                        )
                    )
        self.detail_krs_service.model.objects.bulk_create(
            detail_objs,
            ignore_conflicts=True
        ) # side effect