"""
Department service – business logic for department CRUD.
"""

from typing import Optional
from app.models.department import Department
from app.repositories.json_repository import JsonRepository


class DepartmentService:
    def __init__(self, repo: JsonRepository[Department]) -> None:
        self._repo = repo

    def list_departments(self) -> list[dict]:
        return [d.to_dict() for d in self._repo.get_all()]

    def get_department(self, department_id: int) -> Optional[dict]:
        department = self._repo.get_by_id(department_id)
        return department.to_dict() if department else None

    def create_department(self, data: dict) -> dict:
        if self._repo.get_by_id(data.get("departmentID")):
            raise ValueError("Department with this ID already exists")

        department = Department(
            departmentID=data["departmentID"],
            departmentName=data["departmentName"],
            location=data["location"],
        )

        self._repo.create(department)
        return department.to_dict()

    def update_department(self, department_id: int, data: dict) -> Optional[dict]:
        existing = self._repo.get_by_id(department_id)

        if existing is None:
            return None

        updated = Department(
            departmentID=department_id,
            departmentName=data.get("departmentName", existing.departmentName),
            location=data.get("location", existing.location),
        )

        self._repo.update(department_id, updated)
        return updated.to_dict()

    def delete_department(self, department_id: int) -> bool:
        return self._repo.delete(department_id)