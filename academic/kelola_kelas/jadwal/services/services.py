from django.db.models import F
from academic.models import (
    Kelas, Dosen
)

# from ... import entity

from ..selectors import selectors
from .dto import (
    Result, SetDosenPengampuRequeestDTO, DosenPengampuTambahDTO
)
# from . import dto

import typing

class SelectedField(typing.TypedDict):
    field: str


class CoordinateValue(typing.TypedDict):
    coordinate: str
    fields: list[SelectedField]
    obj: object
    
class KelasSlot(typing.TypedDict):
    kelas_id: int
    field: str

from shared.excel.excel_services import ExcelService, angka_ke_romawi

obj_fields = [
    {"field": "mata_kuliah_nama"},
    {"field": "mata_kuliah_sks"},
    {"field": "mata_kuliah_smt"},
    {"field": "kelas_nama"},
    {"field": "dosen_nama"},
    {"field": "kelas_ruangan"},
]
def kelas_slot_to_coordinate_value(*, kelas_slot_selected: list[KelasSlot]) -> list[CoordinateValue]:
    kelas_selected = (
        Kelas.objects
        .filter(id__in=[slot["kelas_id"] for slot in kelas_slot_selected])
        .select_related("mata_kuliah", "dosen")
        .values(
            "id", 
            kelas_nama=F("nama"), 
            kelas_ruangan=F("ruangan"), 
            dosen_nama=F("dosen__nama"), 
            mata_kuliah_nama= F("mata_kuliah__nama"), 
            mata_kuliah_sks=F("mata_kuliah__sks"), 
            mata_kuliah_smt=F("mata_kuliah__semester")
        )
    )
    
    kelas_by_id = {
        kelas["id"]: kelas
        for kelas in kelas_selected
    }
    # print(kelas_by_id)
    # print(len(kelas_slot_selected))
    # for slot in kelas_slot_selected:
    #     print(slot["kelas_id"]) 
    
    for kelas in kelas_selected:
        if (kelas["id"] == 0):
            print(kelas["id"], kelas["mata_kuliah_nama"])
        # print(kelas["id"], kelas["mata_kuliah_nama"])
    
    
    hasil: list[CoordinateValue] = [
        {
            # "obj": kelas_by_id[slot["kelas_id"]],
            "coordinate": slot["field"],
            "obj": {
                **kelas_by_id[slot["kelas_id"]],
                "mata_kuliah_nama": kelas_by_id[slot["kelas_id"]]["mata_kuliah_nama"].upper(),
                "mata_kuliah_smt": angka_ke_romawi(kelas_by_id[slot["kelas_id"]]["mata_kuliah_smt"]),
                "dosen_nama": kelas_by_id[slot["kelas_id"]]["dosen_nama"] if kelas_by_id[slot["kelas_id"]]["dosen_nama"] else "",
            },
            "fields": obj_fields
        }
        for slot in kelas_slot_selected
        if slot["kelas_id"] in kelas_by_id
    ]
    
    return hasil

class KelasSlotService:
    @staticmethod
    def get_kelas_slot(*, kelas_id: int, slot_id: int):
        pass
    
    @staticmethod
    def tambah_dosen_pengampu(*, dto: DosenPengampuTambahDTO) -> Result:
        if isinstance(dto, dict):
            dto = DosenPengampuTambahDTO(**dto)
        dosen = Dosen.objects.create(nama=dto.nama, no_hp=dto.no_hp, nip=dto.nip)
        return Result(is_success=True, data=dosen)
    
    @staticmethod
    def set_dosen_pengampu(*, dto: SetDosenPengampuRequeestDTO) -> Result:
        if isinstance(dto, dict):
            dto = SetDosenPengampuRequeestDTO(**dto)
        kelas = Kelas.objects.get(id=dto.kelas_id)
        dosen = Dosen.objects.get(id=dto.dosen_id)
        kelas.dosen = dosen
        kelas.save()
        return Result(is_success=True, data=dto)
    
    @staticmethod
    def hapus_dosen_pengampu(*, kelas_id) -> Result:
        
        kelas = Kelas.objects.get(id=kelas_id)
       
        kelas.dosen = None
        kelas.save()
        return Result(is_success=True)
    
    @staticmethod
    def get_slot() -> Result:
        _, meta = selectors.get_slot()
        return Result(is_success=True, data=meta)
    
    @staticmethod
    def download(*, template_jadwal, kelas_slot_selected) -> Result:
        # kelas_slot_selected: list[KelasSlot] = [
        #     {"kelas_id": 130, "field": "C6"},
        #     {"kelas_id": 129, "field": "C7"},
        #     {"kelas_id": 131, "field": "C8"},
        #     {"kelas_id": 132, "field": "C47"},
        #     {"kelas_id": 133, "field": "C54"},
        # ]
        # kelas_slot_selected = [{'kelas_id': 130, 'field': 'C6'}]
        values = kelas_slot_to_coordinate_value(kelas_slot_selected=kelas_slot_selected)
        wb_jadwal, meta_jadwal = ExcelService.load_template(template_jadwal)
        ws_jadwal = wb_jadwal["template"]
        
        ExcelService.sisipkan_nilai(
            ws_jadwal,
            values=values,
            obj_is_dict=True
        )
        
        # hapus sheet meta
        wb_jadwal.remove(wb_jadwal["meta"])

        hasil_bytes = ExcelService.simpan_excel(wb_jadwal)
        
        return Result(is_success=True, data=hasil_bytes)
        