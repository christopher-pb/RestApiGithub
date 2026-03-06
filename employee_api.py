from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {
        "EmployeeID": 1,
        "FirstName": "John",
        "LastName": "Doe",
        "Gender": "Male",
        "DateOfBirth": "1995-05-10"
    }
]

departments = [
    {
        "DepartmentID": 1,
        "DepartmentName": "IT",
        "Location": "Bangalore"
    }
]

salaries = [
    {
        "SalaryID": 1,
        "EmployeeID": 1,
        "BasicSalary": 50000,
        "Bonus": 5000,
        "Allowances": 2000
    }
]

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
    employees.append(data)
    return {"message": "Employee added"}

@app.route("/departments", methods=["GET"])
def get_departments():
    return jsonify(departments)

@app.route("/salaries", methods=["GET"])
def get_salaries():
    return jsonify(salaries)

if __name__ == "__main__":
    app.run(debug=True)