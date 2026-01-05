from datetime import date, timedelta
import pytest
from src.models import Trip
from src.logic import determine_phase, Phase

# Helper to create a trip
def create_trip(
    flight_out="2026-02-14",
    ski_start="2026-02-15",
    ski_end="2026-02-21",
    flight_back="2026-02-22"
):
    return Trip(
        resort_name="Test Resort",
        flight_out_date=date.fromisoformat(flight_out),
        ski_start_date=date.fromisoformat(ski_start),
        ski_end_date=date.fromisoformat(ski_end),
        flight_back_date=date.fromisoformat(flight_back),
        lat=0.0,
        lon=0.0,
        road_check="check"
    )

TRIP = create_trip() # Out: Feb 14, Ski: 15-21, Back: 22

def test_wait_phase():
    # > 90 days before Feb 14
    # 91 days before Feb 14 is Nov 15 2025
    d = date(2025, 11, 15)
    assert determine_phase(TRIP, d) == Phase.WAIT

def test_planning_weekly_boundary():
    # 90 days before -> PLANNING
    d = date(2025, 11, 16) # Nov 16 to Feb 14 ... roughly 90 days
    # Let's verify exact days
    # Feb 14 - Nov 16
    # 30-16 = 14 (Nov) + 31 (Dec) + 31 (Jan) + 14 (Feb) = 90
    assert determine_phase(TRIP, d) == Phase.PLANNING_WEEKLY

def test_hype_daily_boundary():
    # 14 days before Feb 14 is Jan 31
    d = date(2026, 1, 31)
    assert determine_phase(TRIP, d) == Phase.HYPE_DAILY
    
    # 15 days before is Jan 30
    d = date(2026, 1, 30)
    assert determine_phase(TRIP, d) == Phase.PLANNING_WEEKLY

def test_logistics_out():
    # 1 day before Feb 14 is Feb 13
    d = date(2026, 2, 13)
    assert determine_phase(TRIP, d) == Phase.LOGISTICS_OUT

def test_flight_out_day():
    # Feb 14. Should be TRAVEL
    d = date(2026, 2, 14)
    assert determine_phase(TRIP, d) == Phase.TRAVEL

def test_active_ski_start():
    # Feb 15
    d = date(2026, 2, 15)
    assert determine_phase(TRIP, d) == Phase.ACTIVE

def test_active_mid_week():
    # Feb 18
    d = date(2026, 2, 18)
    assert determine_phase(TRIP, d) == Phase.ACTIVE

def test_logistics_back_overrides_active():
    # Flight back Feb 22. Logistics Back is Feb 21.
    # Ski end is Feb 21.
    # So on Feb 21, we are skiing AND 1 day before flight back.
    # Logic: Logistics Back check comes before Active?
    # Logic implementation:
    # 1. Post check
    # 2. Logistics Back check (delta_back == 1) -> Returns LOGISTICS_BACK
    # 3. Active check
    d = date(2026, 2, 21)
    assert determine_phase(TRIP, d) == Phase.LOGISTICS_BACK

def test_travel_back_day():
    # Feb 22
    d = date(2026, 2, 22)
    # Not active (Ski End 21), delta_back=0 != 1.
    # Should fall to TRAVEL
    assert determine_phase(TRIP, d) == Phase.TRAVEL

def test_post_trip():
    # Feb 23
    d = date(2026, 2, 23)
    assert determine_phase(TRIP, d) == Phase.POST

def test_gap_day_wait():
    # Test gap between flight out and ski start if wider
    # Out: 14, Ski: 16 (15 is gap)
    t = create_trip(flight_out="2026-02-14", ski_start="2026-02-16", ski_end="2026-02-21", flight_back="2026-02-22")
    # Feb 15
    # Not Active (starts 16)
    # Not Logistics Out (was 13)
    # Not Logistics Back
    # Falls to "Flight Days or Gap Days" -> TRAVEL
    d = date(2026, 2, 15)
    assert determine_phase(t, d) == Phase.TRAVEL
