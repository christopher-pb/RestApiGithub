"""
Tests for /api/v1/employees endpoints.
"""

SAMPLE_EMPLOYEE = {
    "employeeID": 101,
    "firstName": "John",
    "lastName": "Doe",
    "gender": "Male",
    "dateOfBirth": "1998-05-12",
}


def test_create_employee(client, auth_headers):
    resp = client.post("/api/v1/employees", json=SAMPLE_EMPLOYEE, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["employee"]["firstName"] == "John"


def test_list_employees(client, auth_headers):
    client.post("/api/v1/employees", json=SAMPLE_EMPLOYEE, headers=auth_headers)

    resp = client.get("/api/v1/employees", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["count"] >= 1


def test_get_employee(client, auth_headers):
    create_resp = client.post("/api/v1/employees", json={
        **SAMPLE_EMPLOYEE,
        "employeeID": 102
    }, headers=auth_headers)

    eid = create_resp.get_json()["employee"]["employeeID"]

    resp = client.get(f"/api/v1/employees/{eid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["employeeID"] == eid


def test_update_employee(client, auth_headers):
    create_resp = client.post("/api/v1/employees", json={
        **SAMPLE_EMPLOYEE,
        "employeeID": 103
    }, headers=auth_headers)

    eid = create_resp.get_json()["employee"]["employeeID"]

    resp = client.put(
        f"/api/v1/employees/{eid}",
        json={"firstName": "Updated"},
        headers=auth_headers,
    )

    assert resp.status_code == 200
    assert resp.get_json()["employee"]["firstName"] == "Updated"


def test_delete_employee(client, auth_headers):
    create_resp = client.post("/api/v1/employees", json={
        **SAMPLE_EMPLOYEE,
        "employeeID": 104
    }, headers=auth_headers)

    eid = create_resp.get_json()["employee"]["employeeID"]

    resp = client.delete(f"/api/v1/employees/{eid}", headers=auth_headers)
    assert resp.status_code == 200

    resp = client.get(f"/api/v1/employees/{eid}", headers=auth_headers)
    assert resp.status_code == 404


def test_employees_require_auth(client):
    resp = client.get("/api/v1/employees")
    assert resp.status_code == 401