from fastapi.testclient import TestClient

from apps.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Senior DevOps App is Running"}


def test_health_check_success(monkeypatch):
    class DummyRedis:
        def __init__(self, *args, **kwargs):
            pass

        def ping(self):
            return True

    class DummyConnection:
        def close(self):
            pass

    monkeypatch.setattr("apps.main.Redis", DummyRedis)
    monkeypatch.setattr("apps.main.connect", lambda *args, **kwargs: DummyConnection())

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_check_failure_returns_http_500(monkeypatch):
    class FailingRedis:
        def __init__(self, *args, **kwargs):
            pass

        def ping(self):
            raise RuntimeError("redis unavailable")

    def failing_connect(*args, **kwargs):
        raise RuntimeError("db unavailable")

    monkeypatch.setattr("apps.main.Redis", FailingRedis)
    monkeypatch.setattr("apps.main.connect", failing_connect)

    response = client.get("/health")
    assert response.status_code == 500
    assert response.json() == {"status": "unhealthy", "redis": "unhealthy", "database": "unhealthy"}
