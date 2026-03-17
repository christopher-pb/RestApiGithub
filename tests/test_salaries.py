"""
Tests for /api/v1/salaries endpoints.
"""

SAMPLE_SALARY = {
    "salaryID": 1,
    "employeeID": 1,
    "basicSalary": 50000,
    "bonus": 5000,
    "allowances": 2000,
}


def test_create_salary(client, auth_headers):
    resp = client.post("/api/v1/salaries", json=SAMPLE_SALARY, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()["salary"]["basicSalary"] == 50000


def test_list_salaries(client, auth_headers):
    client.post("/api/v1/salaries", json=SAMPLE_SALARY, headers=auth_headers)

    resp = client.get("/api/v1/salaries", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["count"] >= 1


def test_get_salary(client, auth_headers):
    create_resp = client.post("/api/v1/salaries", json={
        **SAMPLE_SALARY,
        "salaryID": 2
    }, headers=auth_headers)

    sid = create_resp.get_json()["salary"]["salaryID"]

    resp = client.get(f"/api/v1/salaries/{sid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["salaryID"] == sid


def test_delete_salary(client, auth_headers):
    create_resp = client.post("/api/v1/salaries", json={
        **SAMPLE_SALARY,
        "salaryID": 3
    }, headers=auth_headers)

    sid = create_resp.get_json()["salary"]["salaryID"]

    resp = client.delete(f"/api/v1/salaries/{sid}", headers=auth_headers)
    assert resp.status_code == 200


def test_salaries_require_auth(client):
    resp = client.get("/api/v1/salaries")
    assert resp.status_code == 401