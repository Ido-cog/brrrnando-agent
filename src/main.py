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
from .integrations.llm import generate_draft, review_draft
from .integrations.whatsapp import send_whatsapp_message
from .integrations.telegram import send_telegram_message
from .discovery import DiscoveryEngine
from .state import (load_state, save_state, get_resort_state, mark_url_seen, 
                    update_last_run, get_seen_trivia, get_seen_challenges,
                    mark_trivia_seen, mark_challenge_seen)
from .extraction import extract_trivia, extract_challenge

def load_trips(path: str = "trips.json") -> List[Trip]:
    if not os.path.exists(path):
        print(f"Trips file not found: {path}")
        return []
        
    with open(path, "r") as f:
        data = json.load(f)
        
    trips = []
    for item in data:
        trips.append(Trip(**item))
    return trips

def main():
    parser = argparse.ArgumentParser(description="Brrrnando Agent")
    parser.add_argument("--mode", choices=["morning", "evening"], required=True, help="Run mode (morning/evening)")
    parser.add_argument("--dry-run", action="store_true", help="Do not send messages, just print output")
    parser.add_argument("--no-state", action="store_true", help="Do not update or save state (seen URLs, etc.)")
    args = parser.parse_args()
    
    tz = pytz.timezone("Asia/Jerusalem")
    now = datetime.now(tz)
    current_date = now.date()
    
    print(f"Running Brrrnando in {args.mode} mode. Date: {current_date}")
    if args.no_state:
        print("State update is DISABLED for this run.")
    
    trips = load_trips()
    if not trips:
        print("No trips configured.")
        return

    discovery_engine = DiscoveryEngine()
    state = load_state()

    for trip in trips:
        phase = determine_phase(trip, current_date)
        print(f"Trip: {trip.resort_name}, Phase: {phase.value}")
        
        if phase in [Phase.WAIT, Phase.POST]:
            print("Skipping trip (inactive phase).")
            continue
            
        if phase == Phase.PLANNING_WEEKLY:
            if now.weekday() != 0: # 0 = Monday
                print("Skipping Weekly update (not Monday).")
                continue
            if args.mode != "morning":
                 print("Skipping Weekly update (not Morning).")
                 continue

        # Get resort-specific state
        resort_state = get_resort_state(state, trip.resort_name)

        # Gather Weather Data
        weather_info = {}
        if phase in [Phase.ACTIVE, Phase.HYPE_DAILY, Phase.LOGISTICS_OUT, Phase.LOGISTICS_BACK, Phase.TRAVEL, Phase.PLANNING_WEEKLY]:
            try:
                if trip.summit_elevation and trip.base_elevation:
                    weather_summit = get_weather_data(trip.lat, trip.lon, trip.summit_elevation)
                    weather_base = get_weather_data(trip.lat, trip.lon, trip.base_elevation)
                    
                    snow_depth_summit = weather_summit.get("current", {}).get("snow_depth", 0)
                    snow_depth_base = weather_base.get("current", {}).get("snow_depth", 0)
                    snowfall_list = weather_summit.get("daily", {}).get("snowfall_sum", [])
                    total_weekly_snow_cm = round(sum(snowfall_list), 1) if snowfall_list else 0
                    
                    weather_info = {
                        "summit_snow_depth": snow_depth_summit,
                        "base_snow_depth": snow_depth_base,
                        "weekly_snowfall_forecast_cm": total_weekly_snow_cm,
                        "temp_summit": weather_summit.get("current", {}).get("temperature_2m"),
                        "wind_summit": weather_summit.get("current", {}).get("wind_speed_10m")
                    }
                else:
                    weather = get_weather_data(trip.lat, trip.lon)
                    current = weather.get("current", {})
                    snowfall_list = weather.get("daily", {}).get("snowfall_sum", [])
                    total_weekly_snow_cm = round(sum(snowfall_list), 1) if snowfall_list else 0
                    weather_info = {
                        "snow_depth": current.get("snow_depth", 0),
                        "temp_current": current.get("temperature_2m"),
                        "wind_current": current.get("wind_speed_10m"),
                        "weekly_snowfall_forecast_cm": total_weekly_snow_cm
                    }
            except Exception as e:
                print(f"Error gathering weather: {e}")

        # Discovery Phase
        print(f"Running discovery for {trip.resort_name}...")
        insights = discovery_engine.discover_insights(trip, phase, resort_state)
        
        if not insights and phase in [Phase.ACTIVE, Phase.HYPE_DAILY]:
            print(f"No new insights found for {trip.resort_name}. Proceeding with weather only.")

        # Drafting Phase
        print(f"Drafting message for {trip.resort_name}...")
        seen_trivia = get_seen_trivia(resort_state)
        seen_challenges = get_seen_challenges(resort_state)
        draft = generate_draft(trip.resort_name, phase.value, weather_info, insights, 
                              seen_trivia, seen_challenges)
        
        if args.dry_run:
            print("\n--- INITIAL DRAFT ---")
            print(draft)
            print("--------------------\n")

        # Review Loop
        final_message = draft
        for attempt in range(2):
            print(f"Reviewing draft (Attempt {attempt + 1})...")
            approved, result = review_draft(final_message, trip.resort_name, phase.value)
            
            if approved:
                print("Draft approved!")
                final_message = result
                break
            else:
                print(f"Draft needs revision: {result}")
                final_message = generate_draft(trip.resort_name, phase.value, weather_info, insights,
                                              seen_trivia, seen_challenges)

        if args.dry_run:
            print(f"\n--- FINAL MESSAGE ({trip.resort_name}) ---")
            print(final_message)
            print("----------------------------------------------\n")
        else:
            print(f"Sending message for {trip.resort_name}...")
            send_whatsapp_message(final_message)
            send_telegram_message(final_message)

        # Update State
        if not args.no_state:
            for ins in insights:
                mark_url_seen(resort_state, ins.url)
            
            # Extract and save trivia/challenge if present
            trivia = extract_trivia(final_message)
            if trivia:
                print(f"Extracted trivia: {trivia[:50]}...")
                mark_trivia_seen(resort_state, trivia)
            
            challenge = extract_challenge(final_message)
            if challenge:
                print(f"Extracted challenge: {challenge[:50]}...")
                mark_challenge_seen(resort_state, challenge)
            
            update_last_run(resort_state)

    # Save state at the end
    if not args.no_state:
        print("Saving state...")
        save_state(state)
    else:
        print("Skipping state save (no-state flag).")

if __name__ == "__main__":
    main()
