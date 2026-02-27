from flask import Blueprint, request, jsonify
# We import the Manager classes we just created in models.py
from app.models.models import EmployeeManager, DepartmentManager, get_data

# This creates a 'blueprint' so the app knows these are API routes
employee_api = Blueprint('employee_api', __name__)

# --- EMPLOYEE ROUTES ---

@employee_api.route('/employees', methods=['GET'])
def get_all_employees():
    """Returns all employees from the JSON file"""
    return jsonify(get_data('employees')), 200

@employee_api.route('/employees', methods=['POST'])
def add_new_employee():
    """Takes JSON from Postman and saves it to employees.json"""
    data = request.get_json()
    new_emp = EmployeeManager.add_employee(
        data['EmployeeID'], 
        data['FirstName'], 
        data['LastName'], 
        data['Gender'], 
        data['DateOfBirth']
    )
    return jsonify({"message": "Employee added!", "data": new_emp}), 201

# --- DEPARTMENT ROUTES ---

@employee_api.route('/departments', methods=['POST'])
def add_new_department():
    """Takes JSON from Postman and saves it to departments.json"""
    data = request.get_json()
    new_dept = DepartmentManager.add_dept(
        data['DepartmentID'], 
        data['DepartmentName'], 
        data['Location']
    )
    return jsonify({"message": "Department added!", "data": new_dept}), 201