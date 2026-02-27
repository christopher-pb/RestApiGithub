class Salary:
    def __init__(self, SalaryID, EmployeeID,
                 BasicSalary, Bonus, Allowances):
        self.SalaryID = SalaryID
        self.EmployeeID = EmployeeID
        self.BasicSalary = BasicSalary
        self.Bonus = Bonus
        self.Allowances = Allowances

    def to_dict(self):
        return self.__dict__