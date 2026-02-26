import uuid


class Department:
    def __init__(self, department_name: str, location: str, department_id: str = None):
        self.department_id = department_id or str(uuid.uuid4())
        self.department_name = department_name
        self.location = location

    def to_dict(self) -> dict:
        return {
            "department_id": self.department_id,
            "department_name": self.department_name,
            "location": self.location,
        }

    @staticmethod
    def from_dict(data: dict):
        return Department(
            department_name=data.get("department_name"),
            location=data.get("location"),
            department_id=data.get("department_id"),
        )