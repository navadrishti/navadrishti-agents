from app.modules.check_ngo_service.schema import CheckNGOServicesRequest
from app.shared.embeddings.query_maker import make_query

def test_make_query_returns_string():
    payload = CheckNGOServicesRequest(
        category="Education",
        location="Uttar Pradesh",
        budget=100000,
        timeline_start="2025-01-01",
        timeline_end="2025-06-01",
        milestones=3
    )

    result = make_query(payload)
    print(result)
    assert isinstance(result, str)

def test_make_query_contains_fields():
    payload = CheckNGOServicesRequest(
        category="Education",
        location="Uttar Pradesh",
        budget=100000,
        timeline_start="2025-01-01",
        timeline_end="2025-06-01",
        milestones=3
    )

    result = make_query(payload)
    print(result)
    assert "Education" in result
    assert "Uttar Pradesh" in result
    assert "100000" in result

def test_make_query_no_empty_fields():
    payload = CheckNGOServicesRequest(
        category="Healthcare",
        location="Bihar",
        budget=50000,
        timeline_start="2025-03-01",
        timeline_end="2025-09-01",
        milestones=2
    )

    result = make_query(payload)
    print(result)
    assert result.strip() != ""
    assert "None" not in result

