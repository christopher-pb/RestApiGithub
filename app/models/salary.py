"""
Salary model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class Salary:
    salaryID: int
    employeeID: int
    basicSalary: float
    bonus: float
    allowances: float

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Salary":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})