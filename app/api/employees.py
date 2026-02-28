from flask import Blueprint, request, jsonify
from app.repositories.json_repository import JsonRepository
# Import all models from your models folder
from app.models.employees import Employee, Department, Salary

employee_bp = Blueprint('employee_api', __name__)

# Initialize the 3 separate repositories for the 3 JSON files
emp_repo = JsonRepository("data/employees.json", Employee)
dept_repo = JsonRepository("data/departments.json", Department)
sal_repo = JsonRepository("data/salaries.json", Salary)

@employee_bp.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    if request.method == 'POST':
        new_emp = Employee.from_dict(request.json)
        emp_repo.create(new_emp)
        return jsonify({"message": "Employee created"}), 201
    return jsonify([e.to_dict() for e in emp_repo.get_all()])

@employee_bp.route('/departments', methods=['GET', 'POST'])
def manage_departments():
    if request.method == 'POST':
        new_dept = Department.from_dict(request.json)
        dept_repo.create(new_dept)
        return jsonify({"message": "Department created"}), 201
    return jsonify([d.to_dict() for d in dept_repo.get_all()])

@employee_bp.route('/salaries', methods=['GET', 'POST'])
def manage_salaries():
    if request.method == 'POST':
        new_sal = Salary.from_dict(request.json)
        sal_repo.create(new_sal)
        return jsonify({"message": "Salary record created"}), 201
    return jsonify([s.to_dict() for s in sal_repo.get_all()])