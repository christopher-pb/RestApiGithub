"""
Employee service – business logic for employee CRUD.
"""

from typing import Optional

from app.models.employees import Employees
from app.repositories.json_repository import JsonRepository


class EmployeeService:
    def __init__(self, repo: JsonRepository[Employees]) -> None:
        self._repo = repo

    def list_employees(self) -> list[dict]:
        return [e.to_dict() for e in self._repo.get_all()]

    def get_employee(self, employee_id: int) -> Optional[dict]:
        employee = self._repo.get_by_id(employee_id)
        return employee.to_dict() if employee else None

    def create_employee(self, data: dict) -> dict:
        # prevent duplicate employeeID
        if self._repo.get_by_id(data.get("employeeID")):
            raise ValueError("Employee with this ID already exists")

        employee = Employees(
            employeeID=data["employeeID"],
            firstName=data["firstName"],
            lastName=data["lastName"],
            gender=data["gender"],
            dateOfBirth=data["dateOfBirth"],
        )

        self._repo.create(employee)
        return employee.to_dict()

    def update_employee(self, employee_id: int, data: dict) -> Optional[dict]:
        existing = self._repo.get_by_id(employee_id)

        if existing is None:
            return None

        updated = Employees(
            employeeID=employee_id,
            firstName=data.get("firstName", existing.firstName),
            lastName=data.get("lastName", existing.lastName),
            gender=data.get("gender", existing.gender),
            dateOfBirth=data.get("dateOfBirth", existing.dateOfBirth),
        )

        self._repo.update(employee_id, updated)

        return updated.to_dict()

    def delete_employee(self, employee_id: int) -> bool:
        return self._repo.delete(employee_id)