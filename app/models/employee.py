from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Employee:
    employee_id: str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: str
    department: str

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "Employee":
        return Employee(
            employee_id=data["employee_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            department=data["department"],
        )