"""
Tests for /api/v1/departments endpoints.
"""

SAMPLE_DEPARTMENT = {
    "departmentID": 1,
    "departmentName": "IT",
    "location": "Bangalore",
}


def test_create_department(client, auth_headers):
    resp = client.post("/api/v1/departments", json=SAMPLE_DEPARTMENT, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()["department"]["departmentName"] == "IT"


def test_list_departments(client, auth_headers):
    client.post("/api/v1/departments", json=SAMPLE_DEPARTMENT, headers=auth_headers)

    resp = client.get("/api/v1/departments", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["count"] >= 1


def test_get_department(client, auth_headers):
    create_resp = client.post("/api/v1/departments", json={
        **SAMPLE_DEPARTMENT,
        "departmentID": 2
    }, headers=auth_headers)

    did = create_resp.get_json()["department"]["departmentID"]

    resp = client.get(f"/api/v1/departments/{did}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["departmentID"] == did


def test_delete_department(client, auth_headers):
    create_resp = client.post("/api/v1/departments", json={
        **SAMPLE_DEPARTMENT,
        "departmentID": 3
    }, headers=auth_headers)

    did = create_resp.get_json()["department"]["departmentID"]

    resp = client.delete(f"/api/v1/departments/{did}", headers=auth_headers)
    assert resp.status_code == 200


def test_departments_require_auth(client):
    resp = client.get("/api/v1/departments")
    assert resp.status_code == 401