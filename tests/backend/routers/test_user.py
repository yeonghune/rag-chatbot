import os

import http

from .test_auth import _login


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _admin_login(client):
    return _login(client, os.environ["ADMIN_NAME"], os.environ["ADMIN_PASSWORD"])


def test_create_user_requires_admin(client):
    admin_login = _admin_login(client)
    admin_token = admin_login.json()["access_token"]

    payload = {"name": "alice", "password": "alice123", "userRole": "user"}
    response = client.post("/api/users/", json=payload, headers=_auth_header(admin_token))
    assert response.status_code == http.HTTPStatus.OK
    data = response.json()
    assert data["name"] == "alice"
    assert data["userRole"] == "user"

    # Regular user cannot create another user
    user_login = _login(client, "alice", "alice123")
    user_token = user_login.json()["access_token"]
    response_forbidden = client.post(
        "/api/users/",
        json={"name": "bob", "password": "bob123", "userRole": "user"},
        headers=_auth_header(user_token),
    )
    assert response_forbidden.status_code == http.HTTPStatus.FORBIDDEN


def test_get_users_and_details(client):
    admin_login = _admin_login(client)
    token = admin_login.json()["access_token"]

    list_response = client.get("/api/users/", headers=_auth_header(token))
    assert list_response.status_code == http.HTTPStatus.OK
    users = list_response.json()
    assert isinstance(users, list)
    assert any(user["name"] == os.environ["ADMIN_NAME"] for user in users)

    admin_id = next(user["userId"] for user in users if user["name"] == os.environ["ADMIN_NAME"])
    detail_response = client.get(f"/api/users/{admin_id}", headers=_auth_header(token))
    assert detail_response.status_code == http.HTTPStatus.OK
    assert detail_response.json()["name"] == os.environ["ADMIN_NAME"]


def test_update_and_activation_flow(client):
    admin_login = _admin_login(client)
    admin_token = admin_login.json()["access_token"]

    create_response = client.post(
        "/api/users/",
        json={"name": "charlie", "password": "charlie123", "userRole": "user"},
        headers=_auth_header(admin_token),
    )
    user_id = create_response.json()["userId"]

    update_response = client.patch(
        f"/api/users/{user_id}",
        json={"password": "newpass123", "userRole": "admin"},
        headers=_auth_header(admin_token),
    )
    assert update_response.status_code == http.HTTPStatus.OK
    assert update_response.json()["userRole"] == "admin"

    deactivate_response = client.delete(
        f"/api/users/{user_id}",
        headers=_auth_header(admin_token),
    )
    assert deactivate_response.status_code == http.HTTPStatus.OK
    assert deactivate_response.json() is True

    activate_response = client.patch(
        f"/api/users/{user_id}/activate",
        headers=_auth_header(admin_token),
    )
    assert activate_response.status_code == http.HTTPStatus.OK
    assert activate_response.json() is True

    # Ensure updated password works
    login_updated = _login(client, "charlie", "newpass123")
    assert login_updated.status_code == http.HTTPStatus.OK
