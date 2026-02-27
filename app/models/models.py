import json
import os

# Helper function to read/write JSON
def get_data(filename):
    file_path = f'data/{filename}.json'
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(f'data/{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)

# Data Structures
class EmployeeManager:
    @staticmethod
    def add_employee(emp_id, first, last, gender, dob):
        employees = get_data('employees')
        new_emp = {
            "EmployeeID": emp_id,
            "FirstName": first,
            "LastName": last,
            "Gender": gender,
            "DateOfBirth": dob
        }
        employees.append(new_emp)
        save_data('employees', employees)
        return new_emp

class DepartmentManager:
    @staticmethod
    def add_dept(dept_id, name, location):
        depts = get_data('departments')
        new_dept = {
            "DepartmentID": dept_id,
            "DepartmentName": name,
            "Location": location
        }
        depts.append(new_dept)
        save_data('departments', depts)
        return new_dept