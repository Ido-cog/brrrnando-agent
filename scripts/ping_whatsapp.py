import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.integrations.whatsapp import send_whatsapp_template

def main():
    print("--- 🚀 WhatsApp Connection Ping ---")
    print("This will send the default 'hello_world' template to the recipient in your .env file.")
    print("This is used to bypass the 24-hour window and verify the API credentials.")
    
    result = send_whatsapp_template()
    if result:
        print("\nIf you received the message, your setup is correct!")
        print("Note: To receive 'text' messages again, make sure to reply to the bot from your phone.")
    else:
        print("\n❌ Failed to send template. Check your credentials.")

if __name__ == "__main__":
    main()
