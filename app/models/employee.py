from dataclasses import dataclass
from typing import Dict


@dataclass
class Employee:
    employee_id: str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: str
    department_id: str

    def to_dict(self) -> Dict:
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "department_id": self.department_id,
        }