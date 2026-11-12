import pytest

from app import create_app

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        "app.forum.routes.get_categories",
        lambda: [
            {
                "id": 1,
                "slug": "general",
                "title": "General Discussion",
                "description": "General conversations.",
            }
        ],
    )

    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Tsumaranai Forum" in response.data
    assert b"General Discussion" in response.data


def test_category_page(client):
    response = client.get("/categories/general")

    assert response.status_code == 200
    assert b"General Discussion" in response.data
    assert b"No topics yet" in response.data


def test_unknown_category(client):
    response = client.get("/categories/nonexistent")

    assert response.status_code == 404
