from dataclasses import dataclass, asdict

@dataclass
class Employee:
    id: str
    first_name: str
    last_name: str
    gender: str
    dob: str
    def to_dict(self):
        return {"EmployeeID": self.id, "FirstName": self.first_name, "LastName": self.last_name, "Gender": self.gender, "DateOfBirth": self.dob}
    @classmethod
    def from_dict(cls, data):
        return cls(id=data.get("EmployeeID"), first_name=data.get("FirstName"), last_name=data.get("LastName"), gender=data.get("Gender"), dob=data.get("DateOfBirth"))

@dataclass
class Department:
    id: str
    department_name: str
    location: str
    def to_dict(self):
        return {"DepartmentID": self.id, "DepartmentName": self.department_name, "Location": self.location}
    @classmethod
    def from_dict(cls, data):
        return cls(id=data.get("DepartmentID"), department_name=data.get("DepartmentName"), location=data.get("Location"))

@dataclass
class Salary:
    id: str
    employee_id: str
    basic_salary: float
    bonus: float
    allowances: float
    def to_dict(self):
        return {"SalaryID": self.id, "EmployeeID": self.employee_id, "BasicSalary": self.basic_salary, "Bonus": self.bonus, "Allowances": self.allowances}
    @classmethod
    def from_dict(cls, data):
        return cls(id=data.get("SalaryID"), employee_id=data.get("EmployeeID"), basic_salary=data.get("BasicSalary"), bonus=data.get("Bonus"), allowances=data.get("Allowances"))