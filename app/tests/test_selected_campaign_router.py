import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.modules.selected_campaigns import router as selected_router


client = TestClient(app)


def _save_payload() -> dict:
    return {
        "company_id": 1,
        "campaign": {
            "title": "ROUTER_SAVE_TEST",
            "description": "Save endpoint test",
            "category": "education",
            "location": "Delhi",
            "budget_inr": 100000,
            "budget_breakdown": {
                "infrastructure": 20000,
                "training": 20000,
                "materials": 20000,
                "monitoring": 20000,
                "contingency": 20000,
            },
            "schedule_vii": "Education",
            "sdg_alignment": [4],
            "start_date": "2026-01-01",
            "end_date": "2026-03-01",
            "impact_metrics": {"beneficiaries": 100, "duration": "6 months"},
            "milestones": [
                {
                    "title": "Kickoff",
                    "description": "Program launch",
                    "duration_weeks": 2,
                    "budget_allocated": 10000,
                    "deliverables": ["launch-plan"],
                }
            ],
        },
    }


def test_save_campaign_endpoint_success(monkeypatch):
    def fake_store(campaign, company_id):
        assert company_id == 1
        assert isinstance(campaign["budget_breakdown"], dict)
        return {
            "id": "00000000-0000-0000-0000-000000000011",
            "title": campaign["title"],
            "status": "draft",
        }

    monkeypatch.setattr(selected_router.sc_service, "store_selected_campaign", fake_store)

    response = client.post("/api/v1/selected-campaign/save_campaign", json=_save_payload())

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "00000000-0000-0000-0000-000000000011"
    assert data["title"] == "ROUTER_SAVE_TEST"
    assert data["status"] == "draft"


def test_save_campaign_endpoint_db_failure(monkeypatch):
    def fake_store(*_, **__):
        raise RuntimeError("db down")

    monkeypatch.setattr(selected_router.sc_service, "store_selected_campaign", fake_store)

    response = client.post("/api/v1/selected-campaign/save_campaign", json=_save_payload())

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to save campaign"


def test_update_campaign_endpoint_success(monkeypatch):
    campaign_id = str(uuid.uuid4())

    def fake_update(campaign_id, updates, company_id):
        assert campaign_id is not None
        assert str(campaign_id)
        assert updates["title"] == "UPDATED_TITLE"
        assert company_id == 1
        return {
            "id": str(campaign_id),
            "title": updates["title"],
            "status": "draft",
        }

    monkeypatch.setattr(selected_router.sc_service, "update_selected_campaign", fake_update)

    response = client.put(
        f"/api/v1/selected-campaign/update_campaign/{campaign_id}",
        json={
            "company_id": 1,
            "campaign_id": campaign_id,
            "campaign": {"title": "UPDATED_TITLE"},
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "UPDATED_TITLE"
    assert response.json()["message"] == "Campaign updated successfully"


def test_update_campaign_invalid_campaign_id():
    response = client.put(
        "/api/v1/selected-campaign/update_campaign/any-path-id",
        json={
            "company_id": 1,
            "campaign_id": "not-a-uuid",
            "campaign": {"title": "UPDATED_TITLE"},
        },
    )

    assert response.status_code == 422


def test_update_campaign_empty_update_rejected():
    campaign_id = str(uuid.uuid4())
    response = client.put(
        f"/api/v1/selected-campaign/update_campaign/{campaign_id}",
        json={
            "company_id": 1,
            "campaign_id": campaign_id,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No fields to update"


def test_update_campaign_db_failure(monkeypatch):
    campaign_id = str(uuid.uuid4())

    def fake_update(*_, **__):
        raise RuntimeError("db down")

    monkeypatch.setattr(selected_router.sc_service, "update_selected_campaign", fake_update)

    response = client.put(
        f"/api/v1/selected-campaign/update_campaign/{campaign_id}",
        json={
            "company_id": 1,
            "campaign_id": campaign_id,
            "campaign": {"title": "UPDATED_TITLE"},
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to update campaign"


def test_non_selected_campaign_routes_regression():
    health_response = client.get("/api/v1/health")
    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    paths = openapi.json().get("paths", {})
    assert "/api/{version}/check-ngo-service/" in paths
    assert "/api/{version}/generate-campaigns" in paths
