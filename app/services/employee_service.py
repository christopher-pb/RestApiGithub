from app.repositories.json_repository import JsonRepository
from app.models.employee import Employee
from app.models.department import Department
from app.models.salary import Salary

# Initialize separate repos with the separate files
# These paths are relative to the root where the app runs
employee_repo = JsonRepository("data/employees.json", Employee)
department_repo = JsonRepository("data/departments.json", Department)
salary_repo = JsonRepository("data/salaries.json", Salary)