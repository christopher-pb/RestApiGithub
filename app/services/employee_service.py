"""
Employee service – business logic for employee CRUD.
"""
import uuid
from typing import Optional, List

from app.models.employee import Employee
from app.repositories.json_repository import JsonRepository


class EmployeeService:
    def __init__(self, repo: JsonRepository[Employee]) -> None:
        self._repo = repo

    def list_employees(self) -> List[dict]:
        """Get all employees as dictionaries"""
        return [e.to_dict() for e in self._repo.get_all()]

    def get_employee(self, employee_id: str) -> Optional[dict]:
        """Get employee by ID as dictionary"""
        print(f"Looking for employee with ID: {employee_id}")
        employee = self._repo.get_by_id(employee_id)
        print(f"Found employee: {employee}")
        return employee.to_dict() if employee else None

    def create_employee(self, data: dict) -> dict:
        """Create a new employee"""
        employee = Employee(
            employeeId=str(uuid.uuid4()),
            firstName=data["firstName"],
            lastName=data["lastName"],
            gender=data["gender"],
            dateOfBirth=data["dateOfBirth"],
            is_active=data.get("is_active", True)
        )
        self._repo.create(employee)
        return employee.to_dict()

    def update_employee(self, employee_id: str, data: dict) -> Optional[dict]:
        """Update an existing employee"""
        existing = self._repo.get_by_id(employee_id)
        if existing is None:
            return None

        updated = Employee(
            employeeId=employee_id,
            firstName=data.get("firstName", existing.firstName),
            lastName=data.get("lastName", existing.lastName),
            gender=data.get("gender", existing.gender),
            dateOfBirth=data.get("dateOfBirth", existing.dateOfBirth),
            is_active=data.get("is_active", existing.is_active)
        )
        self._repo.update(employee_id, updated)
        return updated.to_dict()

    def delete_employee(self, employee_id: str) -> bool:
        """Delete an employee"""
        return self._repo.delete(employee_id)