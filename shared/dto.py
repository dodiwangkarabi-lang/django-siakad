from dataclasses import dataclass

@dataclass(frozen=True)
class Result:
    is_success: bool
    data: any = None
    errors: dict[str, list[str]] | None = None
    messages: str | None = None