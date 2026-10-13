# import exceptions

class KRSException(Exception):
    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        
        super().__init__(message)
        
# cara pemakaian

# raise KRSException("message", "field")
# cara menangkap errorr

# except KRSException as e:
#     print(e.message)
#     print(e.field)