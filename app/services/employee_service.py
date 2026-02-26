"""
Employee service – business logic for employee CRUD.
"""
import uuid
from typing import Optional

from app.models.employee import Employee
from app.repositories.json_repository import JsonRepository


class EmployeeService:
    def __init__(self, repo: JsonRepository[Employee]) -> None:
        self._repo = repo

    def list_employees(self) -> list[dict]:
        return [e.to_dict() for e in self._repo.get_all()]

    def get_employee(self, employee_id: str) -> Optional[dict]:
        employee = self._repo.get_by_id(employee_id)
        return employee.to_dict() if employee else None

    def create_employee(self, data: dict) -> dict:
        employee = Employee(
            id=str(uuid.uuid4()),
            first_name=data["first_name"],
            last_name=data["last_name"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            department=data["department"],
            salary=data["salary"],
        )
        self._repo.create(employee)
        return employee.to_dict()

    def update_employee(self, employee_id: str, data: dict) -> Optional[dict]:
        existing = self._repo.get_by_id(employee_id)
        if existing is None:
            return None

        updated = Employee(
            id=employee_id,
            first_name=data.get("first_name", existing.first_name),
            last_name=data.get("last_name", existing.last_name),
            gender=data.get("gender", existing.gender),
            date_of_birth=data.get("date_of_birth", existing.date_of_birth),
            department=data.get("department", existing.department),
            salary=data.get("salary", existing.salary),
            created_at=existing.created_at,
            is_active=data.get("is_active", existing.is_active),
        )

        self._repo.update(employee_id, updated)
        return updated.to_dict()

    def delete_employee(self, employee_id: str) -> bool:
        return self._repo.delete(employee_id)