from dataclasses import dataclass

@dataclass
class ValidasiDTO:
    keterangan: str
    status: str
    
    
@dataclass
class ResultDTO:
    is_success: bool
    data: any = ""
    errors: any= ""
    messages: str = ""