import http

def _login(client, username: str, password: str):
    return client.post(
        "/api/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def test_login_success(client, admin_credentials):
    response = _login(client, **admin_credentials)
    assert response.status_code == http.HTTPStatus.OK
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["user"]["name"] == admin_credentials["username"]
    assert "access_token" in payload
    assert response.cookies.get("refresh_token")


def test_login_invalid_password(client, admin_credentials):
    wrong = {**admin_credentials, "password": "incorrect"}
    response = _login(client, **wrong)
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert "refresh_token" not in response.cookies


def test_refresh_token_rotation(client, admin_credentials):
    login_response = _login(client, **admin_credentials)
    refresh_token = login_response.cookies.get("refresh_token")
    access_token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == http.HTTPStatus.OK
    assert me_response.json()["name"] == admin_credentials["username"]

    refresh_response = client.post(
        "/api/auth/refresh",
        cookies={"refresh_token": refresh_token},
    )

    assert refresh_response.status_code == http.HTTPStatus.OK
    refreshed = refresh_response.json()
    assert refreshed["access_token"] != access_token
    assert refresh_response.cookies.get("refresh_token")


def test_logout_current_session_revokes_cookie(client, admin_credentials):
    login_response = _login(client, **admin_credentials)
    refresh_token = login_response.cookies.get("refresh_token")

    logout_response = client.post(
        "/api/auth/logout",
        cookies={"refresh_token": refresh_token},
    )
    assert logout_response.status_code == http.HTTPStatus.OK
    assert logout_response.cookies.get("refresh_token") in ("", None)

    refresh_after_logout = client.post(
        "/api/auth/refresh",
        cookies={"refresh_token": refresh_token},
    )
    assert refresh_after_logout.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_all_sessions_revokes_other_sessions(client, admin_credentials):
    first_login = _login(client, **admin_credentials)
    first_cookie = first_login.cookies.get("refresh_token")

    second_login = _login(client, **admin_credentials)
    second_cookie = second_login.cookies.get("refresh_token")

    logout_all = client.post(
        "/api/auth/logout/all",
        cookies={"refresh_token": second_cookie},
    )
    assert logout_all.status_code == http.HTTPStatus.OK

    for cookie in (first_cookie, second_cookie):
        response = client.post(
            "/api/auth/refresh",
            cookies={"refresh_token": cookie},
        )
        assert response.status_code == http.HTTPStatus.UNAUTHORIZED
