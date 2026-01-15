import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def get_telegram_updates():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        print("1. Create a bot using @BotFather on Telegram.")
        print("2. Add the token to your .env file.")
        return

    print(f"--- 🧩 Fetching Telegram Updates ---")
    print("Action required: Send a message to your bot on Telegram now.")
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    for _ in range(10): # Try for 30 seconds
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    chat = update.get("message", {}).get("chat", {})
                    chat_id = chat.get("id")
                    title = chat.get("title") or chat.get("username") or chat.get("first_name")
                    print(f"\n✅ Found Chat ID!")
                    print(f"Target: {title}")
                    print(f"Chat ID: {chat_id}")
                    print(f"\nUpdate your .env or GHA Secrets with: TELEGRAM_CHAT_ID={chat_id}\n")
                    return
            
            print("Waiting for message... (3s)")
            time.sleep(3)
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print("\n❌ No messages found. Make sure you sent a message to the bot recently.")

if __name__ == "__main__":
    get_telegram_updates()
