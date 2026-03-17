"""
Department model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class Department:
    departmentID: int
    departmentName: str
    location: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})