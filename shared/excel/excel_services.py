from pathlib import Path
from io import BytesIO
import io

import typing

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import column_index_from_string
from openpyxl.utils.cell import coordinate_to_tuple

import pandas as pd

def angka_ke_romawi(angka: int) -> str:
    romawi = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    return romawi[angka - 1]

# SEMESTER = {
#     1: "I",
#     2: "II",
#     3: "III",
#     4: "IV",
#     5: "V",
#     6: "VI",
#     7: "VII",
# }

class SelectedField(typing.TypedDict):
    field: str


class CoordinateValue(typing.TypedDict):
    coordinate: str
    fields: list[SelectedField]
    obj: object
    


class ExcelService:
    def __init__(self):
        pass

    @staticmethod
    def simpan_excel(wb) -> io.BytesIO:
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def sisipkan_array(
        ws, *, kolom: str, data: list, baris_awal: int = 1, coordinate=None
    ):
        if coordinate:
            baris, kolom = coordinate_to_tuple(coordinate=coordinate)

            for row, value in enumerate(data, start=baris):
                ws.cell(row=row, column=kolom, value=value)
        else:
            nomor_kolom = column_index_from_string(kolom)

            for row, value in enumerate(data, start=baris_awal):
                ws.cell(row=row, column=nomor_kolom, value=value)

    @staticmethod
    def sisipkan_nilai_by_coordinat(ws, *, coordinate: str, value: str):
        baris, kolom = coordinate_to_tuple(coordinate=coordinate)

        ws.cell(row=baris, column=kolom, value=value)
        
    
    @staticmethod
    def load_template(template_path: Path) -> Worksheet:
        """
        load template

        Args:
            template_path (Path): lokasi template
            template harus memiliki sheet dengan nama "template" dan "meta"
            di meta terdapat sebuah tabel

        Returns:
            (workbook, meta)
        """
        wb_template = load_workbook(template_path, data_only=True)
        # ws_template: Worksheet = wb_template["template"]

        meta_template = pd.read_excel(template_path, sheet_name="meta")
        meta_template
        meta_list_dict = meta_template.to_dict(orient="records")
        
        return (wb_template, meta_list_dict)
    
    @staticmethod
    def sisipkan_nilai(
        ws,
        *,
        values: list[CoordinateValue],
        obj_is_dict: bool = False,
        kolom_idx: list = [0, 3, 4, 5, 6, 10]
    ) -> None:
        for item in values:
            baris, kolom = coordinate_to_tuple(item["coordinate"])

            # temp = (0, 3, 4, 5, 6, 10) # lokasi kolom
            for kolom_id, field in enumerate(item["fields"]):
                if obj_is_dict:
                    nilai = item["obj"].get(field["field"])
                else:
                    nilai = getattr(item["obj"], field["field"])
                
                kolom_real = kolom_idx[kolom_id] + kolom

                ws.cell(
                    row=baris,
                    column=kolom_real,
                    # column=kolom + kolom_id,
                    value=nilai,
                )
                
# kelas_slot_selected: list[KelasSlot] = [
#     {"kelas_id": 130, "field": "C6"},
#     {"kelas_id": 129, "field": "C7"},
#     {"kelas_id": 131, "field": "C8"},
#     {"kelas_id": 132, "field": "C9"},
#     {"kelas_id": 133, "field": "C10"},
# ]

class JadwalService:
    def __init__(self):
        pass
