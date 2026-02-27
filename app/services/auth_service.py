"""
Authentication service – business logic for login / register.
"""
import uuid
from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.user import User
from app.repositories.json_repository import JsonRepository


class AuthService:
    def __init__(self, repo: JsonRepository[User]) -> None:
        self._repo = repo

    def register(self, username: str, password: str, role: str = "user") -> dict:
        # Check duplicate username
        if self._repo.get_by_field("username", username):
            raise ValueError("Username already exists")

        # Hash password properly
        hashed_password = User.hash_password(password)

        user = User(
            id=str(uuid.uuid4()),
            username=username,
            password_hash=hashed_password,
            role=role,
        )

        # ✅ IMPORTANT: your repository uses create(), not add()
        self._repo.create(user)

        return user.to_dict()

    def login(self, username: str, password: str) -> Optional[dict]:
        user = self._repo.get_by_field("username", username)

        if user is None:
            return None

        if not user.verify_password(password):
            return None

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "role": user.role,
                "username": user.username,
            },
        )

        refresh_token = create_refresh_token(identity=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }