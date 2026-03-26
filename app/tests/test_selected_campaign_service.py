import uuid

import pytest
from fastapi import HTTPException

from app.modules.selected_campaigns.service import SelectedCampaignsService
from app.shared.clients.supabase_client import supabase

scs = SelectedCampaignsService()


def _campaign_payload(title: str = "TEST_CAMPAIGN") -> dict:
    return {
        "title": title,
        "description": "Testing DB insert",
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
        "impact_metrics": {
            "beneficiaries": 100,
            "duration": "6 months",
        },
        "milestones": [
            {
                "title": "Kickoff",
                "description": "Program launch",
                "duration_weeks": 2,
                "budget_allocated": 10000,
                "deliverables": ["launch-plan"],
            }
        ],
        "start_date": "2026-01-01",
        "end_date": "2026-03-01",
    }

def test_store_selected_campaign_inserts_data():
    company_id = 1
    campaign = _campaign_payload()
    inserted_id = None

    #call function
    inserted = scs.store_selected_campaign(campaign, company_id)
    inserted_id = inserted["id"]

    #basic checks
    assert inserted is not None
    assert inserted["title"] == "TEST_CAMPAIGN"
    assert inserted["company_id"] == company_id

    # fetch from DB (real verification)
    db_response = (
        supabase.table("campaigns")
        .select("*")
        .eq("id", inserted["id"])
        .execute()
    )

    assert len(db_response.data) == 1

    row = db_response.data[0]

    # field-level checks
    assert row["title"] == campaign["title"]
    assert row["category"] == campaign["category"]
    assert row["location"] == campaign["location"]
    assert row["budget_inr"] == campaign["budget_inr"]
    assert isinstance(row["budget_breakdown"], dict)
    assert isinstance(row["sdg_alignment"], list)
    assert isinstance(row["impact_metrics"], dict)
    assert isinstance(row["milestones"], list)
    assert row["company_id"] == company_id

    # cleanup (important)
    if inserted_id:
        (
            supabase.table("campaigns")
            .delete()
            .eq("id", inserted_id)
            .execute()
        )


def test_update_selected_campaign_updates_data():
    company_id = 1
    inserted_id = None

    base_campaign = _campaign_payload(title=f"UPDATE_BASE_{uuid.uuid4().hex[:8]}")
    inserted = scs.store_selected_campaign(base_campaign, company_id)
    inserted_id = inserted["id"]

    updates = {
        "title": "UPDATED_CAMPAIGN",
        "budget_inr": 120000,
        "impact_metrics": {"beneficiaries": 150, "duration": "8 months"},
        "milestones": [
            {
                "title": "Review",
                "description": "Mid-term review",
                "duration_weeks": 1,
                "budget_allocated": 8000,
                "deliverables": ["review-report"],
            }
        ],
    }

    updated = scs.update_selected_campaign(str(inserted_id), updates, company_id)

    assert updated["id"] == inserted_id
    assert updated["title"] == updates["title"]
    assert updated["budget_inr"] == updates["budget_inr"]
    assert updated["impact_metrics"] == updates["impact_metrics"]

    db_response = (
        supabase.table("campaigns")
        .select("*")
        .eq("id", inserted_id)
        .execute()
    )
    assert len(db_response.data) == 1

    row = db_response.data[0]
    assert row["title"] == updates["title"]
    assert row["budget_inr"] == updates["budget_inr"]
    assert row["impact_metrics"] == updates["impact_metrics"]
    assert row["milestones"] == updates["milestones"]
    assert row["company_id"] == company_id

    if inserted_id:
        (
            supabase.table("campaigns")
            .delete()
            .eq("id", inserted_id)
            .execute()
        )


def test_store_selected_campaign_payload_mapping_with_mocks(monkeypatch):
    captured = {}

    class FakeResponse:
        def __init__(self, data):
            self.data = data

    class FakeInsertOp:
        def insert(self, payload):
            captured.update(payload)
            return self

        def execute(self):
            return FakeResponse(
                [
                    {
                        "id": "00000000-0000-0000-0000-000000000001",
                        "title": captured["title"],
                        "status": "draft",
                        "company_id": captured["company_id"],
                    }
                ]
            )

    class FakeSupabase:
        def table(self, _):
            return FakeInsertOp()

    monkeypatch.setattr("app.modules.selected_campaigns.service.supabase", FakeSupabase())

    payload = _campaign_payload()
    result = scs.store_selected_campaign(payload, company_id=22)

    assert result["company_id"] == 22
    assert captured["title"] == payload["title"]
    assert captured["budget_inr"] == payload["budget_inr"]
    assert isinstance(captured["budget_breakdown"], dict)
    assert isinstance(captured["sdg_alignment"], list)
    assert isinstance(captured["impact_metrics"], dict)
    assert isinstance(captured["milestones"], list)
    assert captured["company_id"] == 22
    assert captured["status"] == "draft"
    assert "budgetBreakdown" not in captured
    assert "scheduleVII" not in captured


def test_store_selected_campaign_raises_when_insert_fails(monkeypatch):
    class FakeResponse:
        def __init__(self, data):
            self.data = data

    class FakeInsertOp:
        def insert(self, _):
            return self

        def execute(self):
            return FakeResponse([])

    class FakeSupabase:
        def table(self, _):
            return FakeInsertOp()

    monkeypatch.setattr("app.modules.selected_campaigns.service.supabase", FakeSupabase())

    with pytest.raises(HTTPException) as exc:
        scs.store_selected_campaign(_campaign_payload(), company_id=1)

    assert exc.value.status_code == 500
    assert exc.value.detail == "Failed to insert campaign"


def test_update_selected_campaign_raises_not_found(monkeypatch):
    class FakeResponse:
        def __init__(self, data):
            self.data = data

    class FakeSelectOp:
        def select(self, _):
            return self

        def eq(self, *_):
            return self

        def execute(self):
            return FakeResponse([])

    class FakeSupabase:
        def table(self, _):
            return FakeSelectOp()

    monkeypatch.setattr("app.modules.selected_campaigns.service.supabase", FakeSupabase())

    with pytest.raises(HTTPException) as exc:
        scs.update_selected_campaign("id", {"title": "x"}, company_id=1)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Campaign not found"


def test_update_selected_campaign_rejects_active_campaign(monkeypatch):
    class FakeResponse:
        def __init__(self, data):
            self.data = data

    class FakeSelectOp:
        def select(self, _):
            return self

        def eq(self, *_):
            return self

        def execute(self):
            return FakeResponse([{"status": "active"}])

    class FakeSupabase:
        def table(self, _):
            return FakeSelectOp()

    monkeypatch.setattr("app.modules.selected_campaigns.service.supabase", FakeSupabase())

    with pytest.raises(HTTPException) as exc:
        scs.update_selected_campaign("id", {"title": "x"}, company_id=1)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Cannot update an active campaign"


def test_update_selected_campaign_raises_when_update_fails(monkeypatch):
    class FakeResponse:
        def __init__(self, data):
            self.data = data

    class FakeUpdateOp:
        def __init__(self):
            self.mode = "select"

        def select(self, _):
            self.mode = "select"
            return self

        def update(self, _):
            self.mode = "update"
            return self

        def eq(self, *_):
            return self

        def execute(self):
            if self.mode == "select":
                return FakeResponse([{"status": "draft"}])
            return FakeResponse([])

    class FakeSupabase:
        def table(self, _):
            return FakeUpdateOp()

    monkeypatch.setattr("app.modules.selected_campaigns.service.supabase", FakeSupabase())

    with pytest.raises(HTTPException) as exc:
        scs.update_selected_campaign("id", {"title": "x"}, company_id=1)

    assert exc.value.status_code == 500
    assert exc.value.detail == "Failed to update campaign"