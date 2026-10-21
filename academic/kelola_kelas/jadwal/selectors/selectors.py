from django.conf import settings
from django.db.models import F, Q, Count
import typing

from .. import serializers

from shared.excel.excel_services import ExcelService, angka_ke_romawi

class KelasSlot(typing.TypedDict):
    kelas_id: int
    field: str
    
class SelectedField(typing.TypedDict):
    field: str


class CoordinateValue(typing.TypedDict):
    coordinate: str
    fields: list[SelectedField]
    obj: object
    

from academic.models import (
    Kelas, Dosen
)

MEDIA_ROOT = settings.MEDIA_ROOT
template_jadwal = MEDIA_ROOT / "template_excel" / "template_jadwal.xlsx"
# template_jadwal.exists()

obj_fields = [
    {"field": "mata_kuliah_nama"},
    {"field": "mata_kuliah_sks"},
    {"field": "mata_kuliah_smt"},
    {"field": "kelas_nama"},
    {"field": "dosen_nama"},
    {"field": "kelas_ruangan"},
]

kelas_slot_selected: list[KelasSlot] = [
    {"kelas_id": 130, "field": "C6"},
    {"kelas_id": 129, "field": "C7"},
    {"kelas_id": 131, "field": "C8"},
    {"kelas_id": 132, "field": "C47"},
    {"kelas_id": 133, "field": "C54"},
]

# ----- selection -----
def dosen_list():
    dosen_qs = (
        Dosen.objects
        .all()
    )
    return dosen_qs


def kelas_list():
    kalas_qs = (
        Kelas.objects
        .select_related("mata_kuliah", "dosen")
        .filter(
            penawarankrs__isnull=False,
            peserta__isnull=False
        )
        .annotate(
            total_mahasiswa=Count("peserta__krs__mahasiswa", distinct=True)
        )
        .distinct()
    )
    return kalas_qs


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
    
    
    hasil: list[CoordinateValue] = [
        {
            # "obj": kelas_by_id[slot["kelas_id"]],
            "coordinate": slot["field"],
            "obj": {
                **kelas_by_id[slot["kelas_id"]],
                "mata_kuliah_nama": kelas_by_id[slot["kelas_id"]]["mata_kuliah_nama"].upper(),
                "mata_kuliah_smt": angka_ke_romawi(kelas_by_id[slot["kelas_id"]]["mata_kuliah_smt"]),
                "dosen_nama": kelas_by_id[slot["kelas_id"]]["dosen_nama"] if kelas_by_id[slot["kelas_id"]]["dosen_nama"] else "Dodiman",
            },
            "fields": obj_fields
        }
        for slot in kelas_slot_selected
    ]
    
    return hasil

# values = kelas_slot_to_coordinate_value(kelas_slot_selected=kelas_slot_selected)
# values

def get_slot(*, path=None):
    if path is None:
        path = settings.MEDIA_ROOT / "template_excel" / "template_jadwal.xlsx"
    wb_jadwal, meta_jadwal = ExcelService.load_template(template_jadwal)
    # ws_jadwal = wb_jadwal["template"]
    return wb_jadwal, meta_jadwal
