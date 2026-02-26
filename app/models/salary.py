import uuid


class Salary:

    def __init__(
        self,
        employee_id: str,
        basic_salary: float,
        bonus: float,
        allowances: float,
        salary_id: str = None,
    ):
        self.salary_id = salary_id or str(uuid.uuid4())
        self.employee_id = employee_id
        self.basic_salary = basic_salary
        self.bonus = bonus
        self.allowances = allowances

    def to_dict(self):
        return {
            "salary_id": self.salary_id,
            "employee_id": self.employee_id,
            "basic_salary": self.basic_salary,
            "bonus": self.bonus,
            "allowances": self.allowances,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            salary_id=data.get("salary_id"),
            employee_id=data.get("employee_id"),
            basic_salary=data.get("basic_salary"),
            bonus=data.get("bonus"),
            allowances=data.get("allowances"),
        )