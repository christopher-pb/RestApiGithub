from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class Salary:
    salaryId: str
    employeeId: str
    basicSalary: float
    bonus: float
    allowances: float
    is_active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Salary:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})