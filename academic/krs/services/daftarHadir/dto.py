from dataclasses import dataclass
import typing

@dataclass
class Result:
    is_success: bool
    data: typing.Any | None = None
    errors: dict[str, list[str]] | None = None
    messages: str | None = None