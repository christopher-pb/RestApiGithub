from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone

@dataclass
class Employee:
    employeeId: str
    firstName: str
    lastName: str
    gender: str
    dateOfBirth: str
    is_active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Employee:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})