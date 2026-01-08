import pytest
from datetime import date
from src.models import Trip
from src.logic import Phase
from src.discovery import DiscoveryEngine, Insight

@pytest.fixture
def mock_trip():
    return Trip(
        resort_name="Val Thorens",
        flight_out_date=date(2026, 2, 14),
        ski_start_date=date(2026, 2, 15),
        ski_end_date=date(2026, 2, 21),
        flight_back_date=date(2026, 2, 22),
        lat=45.2983,
        lon=6.5824,
        road_check="check"
    )

def test_discover_insights_active(mock_trip):
    engine = DiscoveryEngine()
    # Mocking search would be better, but let's test the orchestration logic
    insights = engine.discover_insights(mock_trip, Phase.ACTIVE)
    assert isinstance(insights, list)
    # Since it's a real search (if API keys are in env), it might return results.
    # In a real CI, we'd mock the integrations.
    
def test_discover_insights_wait(mock_trip):
    engine = DiscoveryEngine()
    insights = engine.discover_insights(mock_trip, Phase.WAIT)
    assert len(insights) == 0
