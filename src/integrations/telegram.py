import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(message: str, chat_id: str = None):
    """
    Send a message via the Telegram Bot API.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    recipient = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    
    if not all([token, recipient]):
        print("Telegram credentials missing (TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID).")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": recipient,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Telegram API Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Message sent successfully to Telegram chat {recipient}")
        else:
            print(f"❌ Message failed to send to Telegram. Status: {response.status_code}")
            print(f"Error details: {response.text}")
            
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error sending Telegram message: {e}")
        return {}

if __name__ == "__main__":
    import sys
    test_msg = "🤖 Brrrnando Telegram Test Message"
    if len(sys.argv) > 1:
        test_msg = " ".join(sys.argv[1:])
    
    print(f"Testing Telegram integration with message: {test_msg}")
    send_telegram_message(test_msg)
