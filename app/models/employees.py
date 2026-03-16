"""
Employees model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Employees:
    employeeID: int
    firstName: str
    lastName: str
    gender: str
    dateOfBirth: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Employees":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})