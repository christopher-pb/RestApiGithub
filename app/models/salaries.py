class Salary:
    def __init__(self, id, employeeId, basicSalary, bonus, allowances):
        self.id = id
        self.employeeId = employeeId
        self.basicSalary = basicSalary
        self.bonus = bonus
        self.allowances = allowances

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["employeeId"],
            data["basicSalary"],
            data["bonus"],
            data["allowances"]
        )