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
        if phase in [Phase.ACTIVE, Phase.HYPE_DAILY, Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK, Phase.TRAVEL]:
            # Weather is relevant for most
            weather = get_weather_data(trip.lat, trip.lon)
            context_data["weather"] = weather
            
        if phase in [Phase.HYPE_DAILY] and args.mode == "evening":
            # Search for videos
            videos = search_videos(f"{trip.resort_name} ski vibe amazing", max_results=2)
            context_data["videos"] = videos
            
        if phase in [Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK] or (phase == Phase.ACTIVE and args.mode == "morning"):
            # Logistics check or Lift Status (Lift status is hard without specific API, use search?)
            # Spec says "Search: current road status".
            if phase in [Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK]:
                roads = search_web(f"Road status {trip.road_check} latest", max_results=3)
                context_data["road_status"] = roads
                
        # Construct Prompt
        prompt = f"""
        You are Brrrnando, a high-energy ski trip agent.
        Write a short, punchy WhatsApp message (use emojis, bold text) for the following context.
        
        Context:
        {json.dumps(context_data, default=str, indent=2)}
        
        Instructions:
        - Mode: {args.mode} (Morning = Live/Brief, Evening = Hype/Forecast).
        - Phase: {phase.value}.
        - If Weekly/Planning: Build hype, mention snow stats.
        - If Hype: Show a video link if available.
        - If Logistics: CRITICAL info on roads/weather.
        - If Active: Morning = Powder alert/Wind chill? Evening = Apre plans/Tomorrow forecast.
        - Keep it under 1000 characters.
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
