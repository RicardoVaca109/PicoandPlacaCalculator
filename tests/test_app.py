# tests/test_app.py
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_main_page_get(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<" in resp.data  # basic check that HTML returned


def test_post_values(client):
    data = {
        "vehicle_plate": "ABC-1231",
        "calculate_date": "2025-10-20",
        "calculate_hour": "07:30",
    }
    resp = client.post("/post_values", data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Pico y Placa" in resp.data
