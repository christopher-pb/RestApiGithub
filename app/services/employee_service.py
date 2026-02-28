import json
import os
from app.models.employee import Employee

DATA_FILE = os.path.join("data", "employees.json")

class EmployeeService:

    @staticmethod
    def get_all():
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_by_id(emp_id):
        employees = EmployeeService.get_all()
        for emp in employees:
            if emp["EmployeeID"] == emp_id:
                return emp
        return None

    @staticmethod
    def add(data):
        employees = EmployeeService.get_all()
        employees.append(data)

        with open(DATA_FILE, "w") as f:
            json.dump(employees, f, indent=4)

        return data

    @staticmethod
    def update(emp_id, new_data):
        employees = EmployeeService.get_all()
        for i, emp in enumerate(employees):
            if emp["EmployeeID"] == emp_id:
                employees[i] = new_data
                with open(DATA_FILE, "w") as f:
                    json.dump(employees, f, indent=4)
                return new_data
        return None

    @staticmethod
    def delete(emp_id):
        employees = EmployeeService.get_all()
        employees = [e for e in employees if e["EmployeeID"] != emp_id]

        with open(DATA_FILE, "w") as f:
            json.dump(employees, f, indent=4)

        return True