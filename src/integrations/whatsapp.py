import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_message(message: str, recipient_id: str = None):
    """
    Send a message via WhatsApp Business Cloud API.
    """
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    recipient = recipient_id or os.getenv("RECIPIENT_PHONE")
    
    if not all([token, phone_id, recipient]):
        print("WhatsApp credentials missing.")
        return
        
    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"WhatsApp API Status: {response.status_code}")
        if response.status_code >= 400:
             print(f"WhatsApp API Error Body: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending WhatsApp message: {e}")
