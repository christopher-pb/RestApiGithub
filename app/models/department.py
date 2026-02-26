from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class Department:
    departmentId: str
    departmentName: str
    location: str
    is_active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Department:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})