from enum import Enum
from datetime import date
from .models import Trip

class Phase(Enum):
    WAIT = "wait"
    PLANNING_WEEKLY = "planning_weekly"
    HYPE_DAILY = "hype_daily"
    LOGISTICS_OUT = "logistics_out"
    ACTIVE = "active"
    LOGISTICS_BACK = "logistics_back"
    POST = "post"
    TRAVEL = "travel" # For flight days if they don't fall into other categories

def determine_phase(trip: Trip, current_date: date) -> Phase:
    delta_out = (trip.flight_out_date - current_date).days
    delta_back = (trip.flight_back_date - current_date).days
    
    # Post trip
    if delta_back < 0:
        return Phase.POST
        
    # Logistics Back: 1 day before flight back
    if delta_back == 1:
        return Phase.LOGISTICS_BACK
        
    # Active Skiing
    if trip.ski_start_date <= current_date <= trip.ski_end_date:
        return Phase.ACTIVE
        
    # Logistics Out: 1 day before flight out
    if delta_out == 1:
        return Phase.LOGISTICS_OUT
        
    # Flight Days or Gap Days (between flight out and ski start, or ski end and flight back)
    # If we are here, we are not skiing, not 1 day before back, not 1 day before out.
    # Check if we are ON the trip (between flight out and flight back inclusive)
    if trip.flight_out_date <= current_date <= trip.flight_back_date:
        return Phase.TRAVEL
        
    # Pre-trip phases
    if delta_out > 90:
        return Phase.WAIT
    
    if 14 < delta_out <= 90:
        return Phase.PLANNING_WEEKLY
        
    if 1 < delta_out <= 14:
        return Phase.HYPE_DAILY
        
    # Should not be reachable if logic is sound, but default to WAIT
    return Phase.WAIT

PHASE_SEARCH_INTENT = {
    Phase.WAIT: [],
    Phase.PLANNING_WEEKLY: ["long range weather", "resort highlights", "ski season outlook"],
    Phase.HYPE_DAILY: ["current snow conditions", "recent instagram videos", "resort news"],
    Phase.LOGISTICS_OUT: ["road status to resort", "airport weather", "transfer tips"],
    Phase.ACTIVE: ["live lift status", "local events today", "best après-ski", "piste map"],
    Phase.LOGISTICS_BACK: ["road status from resort", "airport weather", "return transfer"],
    Phase.TRAVEL: ["airport lounge", "flight status", "travel tips"],
    Phase.POST: ["season recap", "next trip ideas"]
}
