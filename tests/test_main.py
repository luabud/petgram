from starlette.testclient import TestClient
from petgram.main import app

client = TestClient(app)


def test_home_status():
    response = client.get("/")
    assert response.status_code == 200
