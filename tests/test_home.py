from app import create_app

def test_home_page(monkeypatch):
    monkeypatch.setattr(
        "app.get_categories",
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

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Tsumaranai Forum" in response.data
    assert b"General Discussion" in response.data