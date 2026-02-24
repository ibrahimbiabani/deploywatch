import pytest

from deploywatch import config

HEADERS = {"X-API-Key": config.DEPLOY_API_KEY}


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_create_requires_key(client):
    resp = client.post("/deployments", json={"service": "api", "version": "1.0", "env": "dev"})
    assert resp.status_code == 401


def test_create_and_list(client):
    payload = {"service": "api", "version": "1.2.0", "env": "staging", "deployed_by": "ci"}
    resp = client.post("/deployments", json=payload, headers=HEADERS)
    assert resp.status_code == 201

    resp = client.get("/deployments?env=staging")
    assert resp.status_code == 200
    assert any(d["version"] == "1.2.0" for d in resp.get_json())


def test_unknown_environment_rejected(client):
    payload = {"service": "api", "version": "1.0", "env": "moon"}
    resp = client.post("/deployments", json=payload, headers=HEADERS)
    assert resp.status_code == 400


@pytest.mark.skip
def test_rollback(client):
    resp = client.post("/deployments/1/rollback?to=1.0.0", headers=HEADERS)
    assert resp.status_code == 200
