"""
User model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class User:
    id: str
    username: str
    password_hash: Optional[str] = None
    role: str = "user"

    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_hash: bool = False) -> dict:
        data = asdict(self)
        if not include_hash:
            data.pop("password_hash", None)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            password_hash=data.get("password_hash"),
            role=data.get("role", "user"),
        )