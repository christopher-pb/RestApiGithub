class Employee:
    def __init__(self, EmployeeID, FirstName, LastName, Gender, DateOfBirth):
        self.EmployeeID = EmployeeID
        self.FirstName = FirstName
        self.LastName = LastName
        self.Gender = Gender
        self.DateOfBirth = DateOfBirth

    def to_dict(self):
        return {
            "EmployeeID": self.EmployeeID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Gender": self.Gender,
            "DateOfBirth": self.DateOfBirth
        }

    @staticmethod
    def from_dict(data):
        return Employee(
            data["EmployeeID"],
            data["FirstName"],
            data["LastName"],
            data["Gender"],
            data["DateOfBirth"]
        )