"""
Salary service – business logic for salary CRUD.
"""

from typing import Optional
from app.models.salary import Salary
from app.repositories.json_repository import JsonRepository


class SalaryService:
    def __init__(self, repo: JsonRepository[Salary]) -> None:
        self._repo = repo

    def list_salaries(self) -> list[dict]:
        return [s.to_dict() for s in self._repo.get_all()]

    def get_salary(self, salary_id: int) -> Optional[dict]:
        salary = self._repo.get_by_id(salary_id)
        return salary.to_dict() if salary else None

    def create_salary(self, data: dict) -> dict:
        if self._repo.get_by_id(data.get("salaryID")):
            raise ValueError("Salary with this ID already exists")

        salary = Salary(
            salaryID=data["salaryID"],
            employeeID=data["employeeID"],
            basicSalary=data["basicSalary"],
            bonus=data["bonus"],
            allowances=data["allowances"],
        )

        self._repo.create(salary)
        return salary.to_dict()

    def update_salary(self, salary_id: int, data: dict) -> Optional[dict]:
        existing = self._repo.get_by_id(salary_id)

        if existing is None:
            return None

        updated = Salary(
            salaryID=salary_id,
            employeeID=data.get("employeeID", existing.employeeID),
            basicSalary=data.get("basicSalary", existing.basicSalary),
            bonus=data.get("bonus", existing.bonus),
            allowances=data.get("allowances", existing.allowances),
        )

        self._repo.update(salary_id, updated)
        return updated.to_dict()

    def delete_salary(self, salary_id: int) -> bool:
        return self._repo.delete(salary_id)