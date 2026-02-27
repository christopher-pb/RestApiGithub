class EmployeeService:

    def __init__(self, repo):
        self.repo = repo

    def list_employees(self):
        return self.repo.get_all()

    def get_employee(self, employee_id):
        return self.repo.get_by_id(employee_id)

    def create_employee(self, data):
        return self.repo.add(data)

    def update_employee(self, employee_id, data):
        return self.repo.update(employee_id, data)

    def delete_employee(self, employee_id):
        return self.repo.delete(employee_id)