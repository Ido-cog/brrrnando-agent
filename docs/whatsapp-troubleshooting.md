# WhatsApp Message Delivery Troubleshooting Guide

## Quick Diagnostics Checklist

### 1. Check Phone Number Format
The recipient phone number must be in **international format without + or spaces**:
- ✅ Correct: `972501234567` (Israel example)
- ❌ Wrong: `+972-50-123-4567` or `050-123-4567`

**Action**: Check your `RECIPIENT_PHONE` secret in GitHub Settings → Secrets

---

### 2. Verify WhatsApp Business Account Setup
Your WhatsApp Business number must be:
- Verified with Meta
- Have a valid payment method (even for free tier)
- Not blocked or restricted

**Action**: Log into [Meta Business Suite](https://business.facebook.com/) and check:
- WhatsApp → Phone Numbers → Status should be "Connected"
- Check for any warnings or restrictions

---

### 3. Check Message Template Approval (If Using Templates)
Currently, your code sends **free-form text messages**, which only work if:
- The recipient has messaged your business number first (opens 24-hour window)
- OR you're using an approved message template

**Action**: Since you're sending scheduled messages, you likely need to use **Message Templates**

---

### 4. Test with Meta's API Explorer
**Step-by-step test**:
1. Go to [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your WhatsApp Business App
3. Get a User Access Token with `whatsapp_business_messaging` permission
4. Try this test call:

```bash
curl -X POST "https://graph.facebook.com/v17.0/YOUR_PHONE_ID/messages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "YOUR_RECIPIENT_NUMBER",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": { "code": "en_US" }
    }
  }'
```

---

### 5. Check GitHub Actions Logs
**Action**: 
1. Go to your GitHub repo → Actions tab
2. Click on the latest workflow run
3. Expand the "Run Agent" step
4. Look for the WhatsApp API response

**What to look for**:
- `WhatsApp API Status: 200` = Success
- `WhatsApp API Status: 400` = Bad request (check phone format)
- `WhatsApp API Status: 401` = Invalid token
- `WhatsApp API Status: 403` = Permission denied
- `WhatsApp API Status: 404` = Phone ID not found

---

## Common Issues & Solutions

### Issue 1: "Message sent" but nothing received
**Likely cause**: Using free-form text without an open conversation window

**Solution**: Switch to using Message Templates for scheduled messages

**Code change needed**: Update `whatsapp.py` to use templates:
```python
data = {
    "messaging_product": "whatsapp",
    "to": recipient,
    "type": "template",
    "template": {
        "name": "daily_ski_update",  # You need to create this template
        "language": {"code": "en"},
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": message}
                ]
            }
        ]
    }
}
```

---

### Issue 2: Rate Limiting
**Symptoms**: First message works, subsequent ones don't

**Solution**: Check your messaging tier limits in Meta Business Suite

---

### Issue 3: Recipient hasn't opted in
**Requirement**: Users must opt-in to receive messages from your business

**Solution**: 
- Have the recipient send any message to your WhatsApp Business number first
- OR use Click-to-WhatsApp ads to get opt-ins

---

## Immediate Next Steps

1. **Check GitHub Actions logs** for the actual API response
2. **Verify phone number format** in your secrets
3. **Test manually** with Meta's API Explorer
4. **Consider creating a Message Template** for scheduled updates

Would you like me to:
- Update the code to use Message Templates?
- Help you create a template in Meta Business Suite?
- Add better error logging to see the exact API response?
