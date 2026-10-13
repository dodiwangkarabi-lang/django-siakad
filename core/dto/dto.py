from dataclasses import dataclass
from typing import Any

@dataclass
class Result:
    is_success: bool
    data: Any = None
    errors: dict = None