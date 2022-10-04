from fastapi import status
from fastapi.testclient import TestClient

from fastapi_instagram_clone.main import app


client = TestClient(app)


def test_get_all_blogs() -> None:
    response = client.get("/blog/all")
    assert response.status_code == status.HTTP_200_OK


def test_auth_error() -> None:
    json = client.post("/token", data={"username": "", "password": ""}).json()
    assert json.get("access_token") is None
    assert json.get("detail")[0].get("msg") == "field required"


def test_auth_success() -> None:
    assert (
        client.post("/token", data={"username": "cat", "password": "cat"})
        .json()
        .get("access_token")
    ) is not None


def test_post_article() -> None:
    access_token = (
        client.post("/token", data={"username": "cat", "password": "cat"})
        .json()
        .get("access_token")
    )
    response = client.post(
        "/article/",
        json={
            "title": "Test article",
            "content": "Test content",
            "published": True,
            "creator_id": 1,
        },
        headers={"Authorization": f"bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("title") == "Test article"
