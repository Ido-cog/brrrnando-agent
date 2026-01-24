
import sys
import os
from datetime import date
from src.integrations.llm import generate_draft

def test_variation_logic():
    print("Running Manual Variation Test...")
    
    # Mock Data
    trip_name = "Test Resort"
    phase_name = "active"
    weather_data = {
        "summit_snow_depth": 150,
        "base_snow_depth": 50,
        "temp_summit": -5,
        "forecast_confidence": "High"
    }
    insights = []
    seen_trivia = []
    seen_challenges = []
    
    # Mocking recent messages with static data to test "Anti-Repetition"
    recent_messages = [
        {
            "message": "Base depth is 50cm. Summit is 150cm. Great skiing today!",
            "timestamp": "2026-01-23T10:00:00",
            "phase": "active",
            "mode": "morning"
        },
        {
            "message": "Update! Base depth still holding at 50cm. Summit 150cm.",
            "timestamp": "2026-01-22T10:00:00",
            "phase": "active",
            "mode": "morning"
        }
    ]
    
    # Test Case 1: End of trip (2 days left) -> Should ignore weekly forecast
    print("\n--- TEST CASE 1: 2 Days Left (Should ignore weekly forecast) ---")
    draft1_prompt = generate_draft(
        trip_name, phase_name, weather_data, insights, 
        seen_trivia, seen_challenges, recent_messages, ski_days_left=2, return_prompt=True
    )
    print("PROMPT GENERATED:")
    print(draft1_prompt)
    
    # Verify the prompt contains the instruction
    if "IGNORE any long-range/weekly forecasts" in draft1_prompt:
        print("\n[SUCCESS] Prompt correctly includes instruction to ignore long-range forecast.")
    else:
        print("\n[FAILURE] Prompt missing instruction to ignore long-range forecast.")

    # Test Case 2: Check for Anti-Repetition logic in Prompt
    if "ANTI-REPETITION: CHECK 'RECENT MESSAGES'" in draft1_prompt:
         print("[SUCCESS] Anti-repetition instruction is present.")
    else:
         print("[FAILURE] Anti-repetition instruction missing.")

if __name__ == "__main__":
    test_variation_logic()
