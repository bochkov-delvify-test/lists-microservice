from starlette.testclient import TestClient


def test_index(client: TestClient):
    response = client.get("/api/v1/index")
    assert response.status_code == 200
    assert len(response.json()["message"]) > 0
