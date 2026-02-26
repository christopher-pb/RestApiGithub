"""
Department service – business logic for department CRUD.
"""
import uuid
from typing import Optional, List

from app.models.department import Department
from app.repositories.json_repository import JsonRepository


class DepartmentService:
    def __init__(self, repo: JsonRepository[Department]) -> None:
        self._repo = repo

    def list_departments(self) -> List[dict]:
        """Get all departments as dictionaries"""
        return [d.to_dict() for d in self._repo.get_all()]

    def get_department(self, department_id: str) -> Optional[dict]:
        """Get department by ID as dictionary"""
        department = self._repo.get_by_id(department_id)
        return department.to_dict() if department else None

    def create_department(self, data: dict) -> dict:
        """Create a new department"""
        department = Department(
            departmentId=str(uuid.uuid4()),
            departmentName=data["departmentName"],
            location=data["location"],
            is_active=data.get("is_active", True)
        )
        self._repo.create(department)
        return department.to_dict()

    def update_department(self, department_id: str, data: dict) -> Optional[dict]:
        """Update an existing department"""
        existing = self._repo.get_by_id(department_id)
        if existing is None:
            return None

        updated = Department(
            departmentId=department_id,
            departmentName=data.get("departmentName", existing.departmentName),
            location=data.get("location", existing.location),
            is_active=data.get("is_active", existing.is_active)
        )
        self._repo.update(department_id, updated)
        return updated.to_dict()

    def delete_department(self, department_id: str) -> bool:
        """Delete a department"""
        return self._repo.delete(department_id)