"""
Salary service – business logic for salary CRUD.
"""
import uuid
from typing import Optional, List

from app.models.salary import Salary
from app.repositories.json_repository import JsonRepository


class SalaryService:
    def __init__(self, repo: JsonRepository[Salary]) -> None:
        self._repo = repo

    def list_salaries(self) -> List[dict]:
        """Get all salaries as dictionaries"""
        return [s.to_dict() for s in self._repo.get_all()]

    def get_salary(self, salary_id: str) -> Optional[dict]:
        """Get salary by ID as dictionary"""
        salary = self._repo.get_by_id(salary_id)
        return salary.to_dict() if salary else None

    def get_salaries_by_employee(self, employee_id: str) -> List[dict]:
        """Get all salaries for a specific employee"""
        try:
            # Get all salaries and filter by employeeId
            all_salaries = self._repo.get_all()
            filtered = [s for s in all_salaries if s.employeeId == employee_id]
            return [s.to_dict() for s in filtered]
        except Exception as e:
            print(f"Error in get_salaries_by_employee: {e}")
            return []

    def create_salary(self, data: dict) -> dict:
        """Create a new salary record"""
        salary = Salary(
            salaryId=str(uuid.uuid4()),
            employeeId=data["employeeId"],
            basicSalary=float(data["basicSalary"]),
            bonus=float(data["bonus"]),
            allowances=float(data["allowances"]),
            is_active=data.get("is_active", True)
        )
        self._repo.create(salary)
        return salary.to_dict()

    def update_salary(self, salary_id: str, data: dict) -> Optional[dict]:
        """Update an existing salary record"""
        existing = self._repo.get_by_id(salary_id)
        if existing is None:
            return None

        updated = Salary(
            salaryId=salary_id,
            employeeId=data.get("employeeId", existing.employeeId),
            basicSalary=float(data.get("basicSalary", existing.basicSalary)),
            bonus=float(data.get("bonus", existing.bonus)),
            allowances=float(data.get("allowances", existing.allowances)),
            is_active=data.get("is_active", existing.is_active)
        )
        self._repo.update(salary_id, updated)
        return updated.to_dict()

    def delete_salary(self, salary_id: str) -> bool:
        """Delete a salary record"""
        return self._repo.delete(salary_id)