import os
from flask import current_app
from app.models.department import Department
from app.repositories.json_repository import JsonRepository


class DepartmentService:

    def __init__(self):
        data_dir = current_app.config["DATA_DIR"]
        self.repository = JsonRepository(
            os.path.join(data_dir, "departments.json"),
            Department
        )

    # ----------------------------
    # CREATE
    # ----------------------------
    def create_department(self, data: dict) -> dict:
        if not data.get("department_name") or not data.get("location"):
            raise ValueError("DepartmentName and Location are required")

        department = Department(
            department_name=data["department_name"],
            location=data["location"]
        )

        # ✅ FIXED HERE
        self.repository.create(department)

        return department.to_dict()

    # ----------------------------
    # READ ALL
    # ----------------------------
    def get_all_departments(self):
        departments = self.repository.get_all()
        return [dept.to_dict() for dept in departments]

    # ----------------------------
    # READ BY ID
    # ----------------------------
    def get_department_by_id(self, department_id: str):
        department = self.repository.get_by_id(department_id)
        return department.to_dict() if department else None

    # ----------------------------
    # UPDATE
    # ----------------------------
    def update_department(self, department_id: str, data: dict):
        department = self.repository.get_by_id(department_id)
        if not department:
            return None

        if "department_name" in data:
            department.department_name = data["department_name"]

        if "location" in data:
            department.location = data["location"]

        self.repository.update(department_id, department)

        return department.to_dict()

    # ----------------------------
    # DELETE
    # ----------------------------
    def delete_department(self, department_id: str) -> bool:
        return self.repository.delete(department_id)