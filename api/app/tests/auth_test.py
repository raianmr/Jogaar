from app.core.security import Token, verify_access_token
from app.data.crud.user import UserRead
from app.tests.conftest import *
from app.tests.testdata import *
from fastapi import status
from fastapi.testclient import TestClient
from pytest import mark


# TODO: translate the requirement of hashing passwords into tests
@mark.parametrize(
    "in_json,out_status",
    [
        (
            {**DUMMY_USERS_DATA[0], "email": "different@email.com"},
            status.HTTP_201_CREATED,
        ),
        (
            DUMMY_USERS_DATA[0],
            status.HTTP_409_CONFLICT,
        ),
    ],
)
def test_create_user(
    in_json: dict, out_status: int, dummy_users: list[dict], client: TestClient
) -> None:
    resp = client.post("/users", json=in_json)

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_201_CREATED:
        _ = UserRead(**resp.json())  # response validation


@mark.parametrize(
    "in_id,out_status",
    [
        (len(DUMMY_USERS_DATA) // 2, status.HTTP_200_OK),
        (len(DUMMY_USERS_DATA) * 2, status.HTTP_404_NOT_FOUND),
    ],
)
def test_read_user(
    in_id: int, out_status: int, dummy_users: list[dict], client: TestClient
) -> None:

    resp = client.get(f"/users/{in_id}")

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_200_OK:
        _ = UserRead(**resp.json())  # response validation


@mark.parametrize(
    "in_limit,in_offset,in_len,out_status",
    [
        (len(DUMMY_USERS_DATA), 0, len(DUMMY_USERS_DATA), status.HTTP_200_OK),
        (len(DUMMY_USERS_DATA) * 2, len(DUMMY_USERS_DATA), 0, status.HTTP_200_OK),
    ],
)
def test_read_users(
    in_limit: int,
    in_offset: int,
    in_len: int,
    out_status: int,
    dummy_users: list[dict],
    client: TestClient,
) -> None:
    resp = client.get(f"/users?limit={in_limit}&offset={in_offset}")

    assert resp.status_code == out_status

    resp_data = resp.json()

    assert len(resp_data) == in_len

    if resp.status_code == status.HTTP_200_OK and len(resp_data) > 0:
        _ = UserRead(**resp.json()[0])  # response validation


# TODO: account for password changes
@mark.parametrize(
    "in_id,in_json,out_status",
    [
        (
            AUTHORIZED_USER_ID,
            {"about": "generic intro", "password": "updated password"},
            status.HTTP_200_OK,
        ),
        (
            AUTHORIZED_USER_ID,
            {"email": DUMMY_USERS_DATA[-1]["email"]},
            status.HTTP_409_CONFLICT,
        ),
        (
            len(DUMMY_USERS_DATA) * 2,
            {"name": "updated name"},
            status.HTTP_404_NOT_FOUND,
        ),
        (
            AUTHORIZED_USER_ID + 1,
            {"contact": "01696969420"},
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_update_user(
    in_id: int,
    in_json: dict,
    out_status: int,
    dummy_users: list[dict],
    authorized_client: TestClient,
) -> None:
    resp = authorized_client.put(f"/users/{in_id}", json=in_json)

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_200_OK:
        resp_data = resp.json()
        resp_validated = UserRead(**resp_data)  # response validation
        merged_validated = UserRead(**{**resp_data, **in_json})

        assert resp_validated == merged_validated  # verify changes


@mark.parametrize(
    "in_id,out_status",
    [
        (AUTHORIZED_USER_ID, status.HTTP_204_NO_CONTENT),
        (len(DUMMY_USERS_DATA) * 2, status.HTTP_404_NOT_FOUND),
        (AUTHORIZED_USER_ID + 1, status.HTTP_403_FORBIDDEN),
    ],
)
def test_delete_user(
    in_id: int, out_status: int, dummy_users: list[dict], authorized_client: TestClient
) -> None:
    resp = authorized_client.delete(f"/users/{in_id}")

    assert resp.status_code == out_status


@mark.parametrize(
    "in_username,in_password,out_status",
    [
        (
            DUMMY_USERS_DATA[0]["email"],
            DUMMY_USERS_DATA[0]["password"],
            status.HTTP_200_OK,
        ),
        (DUMMY_USERS_DATA[0]["email"], "wrong password", status.HTTP_401_UNAUTHORIZED),
        (
            "wrong username",
            DUMMY_USERS_DATA[0]["password"],
            status.HTTP_401_UNAUTHORIZED,
        ),
    ],
)
def test_login_user(
    in_username: str,
    in_password: str,
    out_status: int,
    dummy_users: list[dict],
    client: TestClient,
) -> None:
    resp = client.post(
        f"/login", data={"username": in_username, "password": in_password}
    )

    assert resp.status_code == out_status

    if resp.status_code == status.HTTP_200_OK:
        resp_data = resp.json()
        token_resp = Token(**resp_data)  # response validation

        token_data = verify_access_token(token_resp.access_token)
        assert token_resp.token_type == "bearer"
