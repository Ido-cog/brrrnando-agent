import argparse
import json
import os
import sys
from datetime import date, datetime
import pytz
from typing import List

from .models import Trip
from .logic import determine_phase, Phase
from .integrations.weather import get_weather_data
from .integrations.search import search_web, search_videos
from .integrations.llm import generate_summary
from .integrations.whatsapp import send_whatsapp_message

def load_trips(path: str = "trips.json") -> List[Trip]:
    if not os.path.exists(path):
        print(f"Trips file not found: {path}")
        return []
        
    with open(path, "r") as f:
        data = json.load(f)
        
    trips = []
    for item in data:
        # Convert string dates to date objects (pydantic does this but we need to feed it dicts)
        trips.append(Trip(**item))
    return trips

def main():
    parser = argparse.ArgumentParser(description="Brrrnando Agent")
    parser.add_argument("--mode", choices=["morning", "evening"], required=True, help="Run mode (morning/evening)")
    parser.add_argument("--dry-run", action="store_true", help="Do not send messages, just print output")
    args = parser.parse_args()
    
    # IST Timezone for logging/logic if needed, but logic uses dates.
    # Current date:
    tz = pytz.timezone("Asia/Jerusalem")
    now = datetime.now(tz)
    current_date = now.date()
    
    print(f"Running Brrrnando in {args.mode} mode. Date: {current_date}")
    
    trips = load_trips()
    if not trips:
        print("No trips configured.")
        return

    for trip in trips:
        phase = determine_phase(trip, current_date)
        print(f"Trip: {trip.resort_name}, Phase: {phase.value}")
        
        if phase in [Phase.WAIT, Phase.POST]:
            print("Skipping trip (inactive phase).")
            continue
            
        # Determine if we should run based on Mode and Phase
        # Weekly: Run only on Morning? Or Evening? Spec says "Weekly update". 
        # Let's pick Morning. And assume Weekly runs on a specific day? 
        # Clarification in spec assumption: "check if current day is Monday".
        if phase == Phase.PLANNING_WEEKLY:
            if now.weekday() != 0: # 0 = Monday
                print("Skipping Weekly update (not Monday).")
                continue
            if args.mode != "morning":
                 print("Skipping Weekly update (not Morning).")
                 continue

        # Active/Hype/Logistics
        # Morning: Live conditions
        # Evening: Forecast + Hype
        
        context_data = {
            "trip": trip.model_dump(),
            "phase": phase.value,
            "mode": args.mode,
            "date": str(current_date)
        }
        
        # Gather Data
        if phase in [Phase.ACTIVE, Phase.HYPE_DAILY, Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK, Phase.TRAVEL, Phase.PLANNING_WEEKLY]:
            # Weather is relevant
            if trip.summit_elevation and trip.base_elevation:
                weather_summit = get_weather_data(trip.lat, trip.lon, trip.summit_elevation)
                weather_base = get_weather_data(trip.lat, trip.lon, trip.base_elevation)
                
                # Combine or structure for LLM
                snow_depth_summit = weather_summit.get("current", {}).get("snow_depth", 0)
                snow_depth_base = weather_base.get("current", {}).get("snow_depth", 0)
                
                # Snowfall forecast (7 days) - assume summit forecast represents the area
                snowfall_list = weather_summit.get("daily", {}).get("snowfall_sum", [])
                total_weekly_snow = sum(snowfall_list) if snowfall_list else 0
                
                context_data["weather"] = {
                    "summit": weather_summit,
                    "base": weather_base,
                    "snow_depth_summit": snow_depth_summit,
                    "snow_depth_base": snow_depth_base,
                    "weekly_snowfall_forecast": total_weekly_snow
                }
            else:
                weather = get_weather_data(trip.lat, trip.lon)
                snowfall_list = weather.get("daily", {}).get("snowfall_sum", [])
                total_weekly_snow = sum(snowfall_list) if snowfall_list else 0
                context_data["weather"] = weather
                context_data["weather"]["weekly_snowfall_forecast"] = total_weekly_snow
            
        if phase in [Phase.HYPE_DAILY] and args.mode == "evening":
            # Search for videos
            videos = search_videos(f"{trip.resort_name} ski vibe amazing", max_results=2)
            context_data["videos"] = videos
            
        if phase in [Phase.ACTIVE, Phase.HYPE_DAILY, Phase.PLANNING_WEEKLY]:
            # Search for Piste Map - Use 'official site' to get better results
            piste_map = search_web(f"{trip.resort_name} official piste map PDF link site", max_results=2)
            context_data["piste_map_info"] = piste_map

        if phase in [Phase.ACTIVE] or (phase == Phase.HYPE_DAILY and args.mode == "evening"):
            # Search for Lift Status - Focus on official resort status
            lifts = search_web(f"{trip.resort_name} live lift status official site opening percentage", max_results=2)
            context_data["lift_status_info"] = lifts
            
        if phase in [Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK] or (phase == Phase.ACTIVE and args.mode == "morning"):
            # Logistics check or Lift Status (Lift status is hard without specific API, use search?)
            # Spec says "Search: current road status".
            if phase in [Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK]:
                roads = search_web(f"Road status {trip.road_check} latest", max_results=3)
                context_data["road_status"] = roads
                
        # Construct Prompt
        prompt = f"""
        You are Brrrnando, an Enthusiastic Ski Specialist. 
        Your tone is vibrant, expert, and alive—but professional. Think of yourself as a high-end ski concierge who is pumped about the mountain but keeps it useful.
        Avoid repetitive "hype" words or being "ridiculous," but don't be dry or "lifeless."

        Write a concise WhatsApp message (use bold text for key stats) for the following context.
        
        Context:
        {json.dumps(context_data, default=str, indent=2)}
        
        Mandatory content to include if available:
        - Snow Depth at Summit and Base (in cm). 
        - 7-Day Snowfall Forecast (total cm). 
        - Temperature and Wind conditions.
        - **Piste Map**: Provide a direct link to the best PDF/official map found in the context.
        - **Lift & Run Status**: Summarize how many lifts/runs are open based on the context. 
          *IMPORTANT*: Never say "info is not available" if there are search results. Instead, give the best summary of what is likely open and point them to the link.
        
        Instructions by Phase:
        - Mode: {args.mode} (Morning = Conditions/Live, Evening = Forecast/Hype).
        - Phase: {phase.value}.
        - If Weekly/Planning: Focus on the 7-day forecast and base/summit snow accumulation.
        - If Hype: Include a video link and the piste map link.
        - If Logistics: Provide clear status on roads and weather.
        - If Active: Morning = Current local conditions + Lift status. Evening = Tomorrow's forecast + Apre plans.
        
        Keep the message under 1000 characters and well-structured with bullet points or bold headers.
        """
        
        if args.dry_run:
            print("\n--- PROMPT ---")
            print(prompt)
            print("----------------")
        
        # Generate
        message = generate_summary(prompt)
        
        if args.dry_run:
            print(f"\n--- GENERATED MESSAGE ({trip.resort_name}) ---")
            print(message)
            print("----------------------------------------------\n")
        else:
            print(f"Sending message for {trip.resort_name}...")
            send_whatsapp_message(message)

if __name__ == "__main__":
    main()
