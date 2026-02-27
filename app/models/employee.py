class Employee:

    def __init__(
        self,
        employee_id,
        first_name,
        last_name,
        gender,
        date_of_birth
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth

    def to_dict(self):
        return self.__dict__