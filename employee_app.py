from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {"EmployeeID": 1, "FirstName": "John", "LastName": "Doe", "Gender": "Male", "DateOfBirth": "1990-01-15"},
    {"EmployeeID": 2, "FirstName": "Jane", "LastName": "Smith", "Gender": "Female", "DateOfBirth": "1992-05-20"}
]

departments = [
    {"DepartmentID": 1, "DepartmentName": "Engineering", "Location": "New York"},
    {"DepartmentID": 2, "DepartmentName": "HR", "Location": "Chicago"}
]

salaries = [
    {"SalaryID": 1, "EmployeeID": 1, "BasicSalary": 60000, "Bonus": 5000, "Allowances": 2000},
    {"SalaryID": 2, "EmployeeID": 2, "BasicSalary": 55000, "Bonus": 4000, "Allowances": 1500}
]

# EMPLOYEES
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    emp = next((e for e in employees if e['EmployeeID'] == emp_id), None)
    return jsonify(emp) if emp else ('Not Found', 404)

@app.route('/employees', methods=['POST'])
def add_employee():
    new_emp = request.json
    new_emp['EmployeeID'] = max(e['EmployeeID'] for e in employees) + 1
    employees.append(new_emp)
    return jsonify(new_emp), 201

@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    emp = next((e for e in employees if e['EmployeeID'] == emp_id), None)
    if not emp:
        return ('Not Found', 404)
    emp.update(request.json)
    return jsonify(emp)

@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    global employees
    employees = [e for e in employees if e['EmployeeID'] != emp_id]
    return ('', 204)

# DEPARTMENTS
@app.route('/departments', methods=['GET'])
def get_departments():
    return jsonify(departments)

@app.route('/departments/<int:dept_id>', methods=['GET'])
def get_department(dept_id):
    dept = next((d for d in departments if d['DepartmentID'] == dept_id), None)
    return jsonify(dept) if dept else ('Not Found', 404)

@app.route('/departments', methods=['POST'])
def add_department():
    new_dept = request.json
    new_dept['DepartmentID'] = max(d['DepartmentID'] for d in departments) + 1
    departments.append(new_dept)
    return jsonify(new_dept), 201

# SALARIES
@app.route('/salaries', methods=['GET'])
def get_salaries():
    return jsonify(salaries)

@app.route('/salaries/<int:emp_id>', methods=['GET'])
def get_salary_by_employee(emp_id):
    sal = next((s for s in salaries if s['EmployeeID'] == emp_id), None)
    return jsonify(sal) if sal else ('Not Found', 404)

@app.route('/salaries', methods=['POST'])
def add_salary():
    new_sal = request.json
    new_sal['SalaryID'] = max(s['SalaryID'] for s in salaries) + 1
    salaries.append(new_sal)
    return jsonify(new_sal), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)