class Employee:
    def __init__(self, id, firstName, lastName, gender, dateOfBirth):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.dateOfBirth = dateOfBirth

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["firstName"],
            data["lastName"],
            data["gender"],
            data["dateOfBirth"]
        )