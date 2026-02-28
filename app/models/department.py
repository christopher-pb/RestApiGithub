class Department:
    def __init__(self, id, departmentName, location):
        self.id = id
        self.departmentName = departmentName
        self.location = location

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["departmentName"],
            data["location"]
        )