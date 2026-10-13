import pymupdf
import pandas as pd

from django.conf import settings
media_root = settings.MEDIA_ROOT
private_dir = media_root / "private" / "krs" / "img"

# ----- dto -----
# from .dto import KRSValues

class CetakService:
    def __init__(self):
        # self.path_template = path_template
        self.meta_doc = None
        self.data_input = None
        self.doc = None
        
    def open_pdf(self, *args, **kwargs):
        """
        buka pdf, bisa menggunakan string, bisa juga menggunakan, bytes

        Returns:
            _type_: _description_
            
        Example:
            cetakService = CetakService()
            cetakService.open_pdf("template.pdf")
            cetakService.load_meta_doc("hasil_app.xlsx", sheet_name="meta_doc")
            cetakService.load_data_input("hasil_app.xlsx", sheet_name="value")
            cetakService.cetak
            
            dari stream
            with open("template.pdf", "rb") as file:
                template_bytes = file.read()
                
            cetakService.open_pdf(stream = template_bytes)
            
        """
        doc = pymupdf.open(*args, **kwargs)
        self.doc = doc
        return self
    
    def close_pdf(self):
        if self.doc:
            self.doc.close()
        return self
    
    def load_meta_doc(self, path, sheet_name):
        df = pd.read_excel(path, sheet_name=sheet_name)
        
        meta_doc = {
            row["field"]: {
                "x": row["x"],
                "y": row["y"],
                "size": row["size"],
                "color": tuple(
                    int(value.strip())
                    for value in str(row["color"]).split(",")
                ),
                "type": row["type"],
            }
            for _, row in df.iterrows()
        }
    
        self.meta_doc = meta_doc
        return self
    
    def set_data_input(self, data_input):
        self.data_input = data_input
        return self
    
    def set_data_input_biodata(self, data_input):
        self.data_input = data_input
        return self
    
    def load_data_input(self, path, sheet_name):
        df = pd.read_excel(path, sheet_name=sheet_name)
        data_input = {
            row["field"]: row["value"]
            for _, row in df.iterrows()
        }
        self.data_input = data_input
        return self
    
    @property
    def cetak(self) -> bytes:
        
        assert self.meta_doc is not None, "meta_doc is not loaded"
        assert self.data_input is not None, "data_input is not loaded"
        # assert self.path_template is not None, "path_template is not loaded"
        
        DATA_INPUT = self.data_input
        meta_doc = self.meta_doc

        # meta_doc = self.load_meta_doc("hasil_app.xlsx", sheet_name="meta_doc")
        # DATA_INPUT = self.load_data_input("hasil_app.xlsx", sheet_name="value")

        # doc = pymupdf.open("template.pdf")
        
        assert self.doc is not None, "doc is not loaded"
        
        with self.doc as doc:
            page = doc[0]

            for key, value in DATA_INPUT.items():
                if meta_doc[key]["type"] == "img":
                    # size = 8
                    size = meta_doc[key]["size"]
                    x = meta_doc[key]["x"]
                    y = meta_doc[key]["y"]

                    width = 100
                    height = 100
                    
                    rect = pymupdf.Rect(
                        x,
                        y,
                        x + size, # width
                        y + size, # height
                    )
                    
                    gambar = private_dir / value
                    if key == "TTD_MAHASISWA":
                        gambar = value
                    
                    page.insert_image(
                        rect,
                        filename=gambar
                    )
                    continue
                page.insert_text(
                    (meta_doc[key]["x"], meta_doc[key]["y"]),
                    value,
                    fontsize=meta_doc[key]["size"],
                    color=meta_doc[key]["color"],
                )
                # print(meta_doc[key])
                
            # doc.save("hasil.pdf")
            return doc.tobytes()
        
        # except Exception as e:
        #     print(e)
        # finally:
        #     doc.close()