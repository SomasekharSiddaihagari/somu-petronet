from fastapi.testclient import TestClient
from app.main import app  # make sure this matches your module structure

client = TestClient(app)

def test_health():
    r = client.get("/healthz")  # hitting new health endpoint
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
