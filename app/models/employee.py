"""
Employee model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class Employee:
    id: str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        return cls(**{
            k: v for k, v in data.items()
            if k in cls.__dataclass_fields__
        })