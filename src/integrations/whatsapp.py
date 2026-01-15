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
    raw_recipient = recipient_id or os.getenv("RECIPIENT_PHONE")
    
    # Sanitize recipient: only digits
    recipient = "".join(filter(str.isdigit, raw_recipient)) if raw_recipient else None
    
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
        print(f"WhatsApp API Response: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Message sent successfully to {recipient}")
        else:
            print(f"❌ Message failed to send. Status: {response.status_code}")
            print(f"Error details: {response.text}")
            
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}")
        return {}

def send_whatsapp_template(template_name: str = "hello_world", language_code: str = "en_US", recipient_id: str = None):
    """
    Send a WhatsApp Template message. Useful for opening the 24h window.
    """
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    raw_recipient = recipient_id or os.getenv("RECIPIENT_PHONE")
    recipient = "".join(filter(str.isdigit, raw_recipient)) if raw_recipient else None

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
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code}
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"WhatsApp Template API Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Template '{template_name}' sent to {recipient}")
        else:
            print(f"❌ Template failed. {response.text}")
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error sending template: {e}")
        return {}
