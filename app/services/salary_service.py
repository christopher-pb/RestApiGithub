from typing import List, Optional
from app.models.salary import Salary
from app.models.employee import Employee
from app.repositories.json_repository import JsonRepository


class SalaryService:

    def __init__(
        self,
        salary_repository: JsonRepository[Salary],
        employee_repository: JsonRepository[Employee],
    ):
        self.salary_repository = salary_repository
        self.employee_repository = employee_repository

    # ----------------------------
    # LIST
    # ----------------------------
    def list_salaries(self) -> List[dict]:
        return [salary.to_dict() for salary in self.salary_repository.get_all()]

    # ----------------------------
    # GET
    # ----------------------------
    def get_salary(self, salary_id: str) -> Optional[dict]:
        salary = self.salary_repository.get_by_id(salary_id)
        return salary.to_dict() if salary else None

    # ----------------------------
    # CREATE
    # ----------------------------
    def create_salary(self, data: dict) -> dict:

        required_fields = [
            "employee_id",
            "basic_salary",
            "bonus",
            "allowances",
        ]

        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")

        # ✅ Validate Employee exists
        employee = self.employee_repository.get_by_id(data["employee_id"])
        if not employee:
            raise ValueError("Employee does not exist")

        salary = Salary(
            employee_id=data["employee_id"],
            basic_salary=float(data["basic_salary"]),
            bonus=float(data["bonus"]),
            allowances=float(data["allowances"]),
        )

        self.salary_repository.create(salary)

        return salary.to_dict()

    # ----------------------------
    # UPDATE
    # ----------------------------
    def update_salary(self, salary_id: str, data: dict) -> Optional[dict]:

        salary = self.salary_repository.get_by_id(salary_id)
        if not salary:
            return None

        for key, value in data.items():
            if hasattr(salary, key):
                setattr(salary, key, value)

        self.salary_repository.update(salary_id, salary)

        return salary.to_dict()

    # ----------------------------
    # DELETE
    # ----------------------------
    def delete_salary(self, salary_id: str) -> bool:
        return self.salary_repository.delete(salary_id)