from academic.models import MataKuliah, Kelas, DetailKRS, KRS
from shared.services import BaseModelService

class MataKuliahService(BaseModelService):
    model = MataKuliah
    
class KelasService(BaseModelService):
    model = Kelas
    
class DetailKRSService(BaseModelService):
    model = DetailKRS
    
class KRSService(BaseModelService):
    model = KRS

