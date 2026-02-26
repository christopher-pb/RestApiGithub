import uuid
from typing import List, Optional
from app.models.employee import Employee
from app.repositories.json_repository import JsonRepository


class EmployeeService:

    def __init__(self, repository: JsonRepository[Employee]):
        self.repository = repository

    def list_employees(self) -> List[dict]:
        return [emp.to_dict() for emp in self.repository.get_all()]

    def get_employee(self, employee_id: str) -> Optional[dict]:
        emp = self.repository.get_by_id(employee_id)
        return emp.to_dict() if emp else None

    def create_employee(self, data: dict) -> dict:

        employee = Employee(
            employee_id=str(uuid.uuid4()),
            first_name=data["first_name"],
            last_name=data["last_name"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            department=data["department"],
        )

        self.repository.create(employee)

        return employee.to_dict()

    def update_employee(self, employee_id: str, data: dict) -> Optional[dict]:

        emp = self.repository.get_by_id(employee_id)

        if not emp:
            return None

        for key, value in data.items():
            if hasattr(emp, key):
                setattr(emp, key, value)

        self.repository.update(employee_id, emp)

        return emp.to_dict()

    def delete_employee(self, employee_id: str) -> bool:
        return self.repository.delete(employee_id)