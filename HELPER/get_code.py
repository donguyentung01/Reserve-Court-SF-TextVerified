import requests
import re
from datetime import datetime, timezone, timedelta
import time 
def get_bearer_token(username, api_key):
    url = "https://www.textverified.com/api/pub/v2/auth"
    headers = {
        "X-API-USERNAME": username,
        "X-API-KEY": api_key
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("token")  # Adjust if needed

def get_sms_list(bearer_token):
    url = "https://www.textverified.com/api/pub/v2/sms"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_latest_message_within_1_min(messages):
    now = datetime.now(timezone.utc)
    ten_minutes_ago = now - timedelta(minutes=1)
    recent_messages = [
        m for m in messages
        if datetime.fromisoformat(m["createdAt"].replace("Z", "+00:00")) >= ten_minutes_ago
    ]
    if not recent_messages:
        return None
    return max(recent_messages, key=lambda m: datetime.fromisoformat(m["createdAt"].replace("Z", "+00:00")))

def extract_verification_code(sms_content):
    match = re.search(r'code is[:\s]+(\d+)', sms_content, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def get_message_time(message):
    return datetime.fromisoformat(message["createdAt"].replace("Z", "+00:00"))

def get_latest_verification_code(username, api_key, from_number, timeout=30, interval=1):
    token = get_bearer_token(username, api_key)
    if not token:
        return None

    start_time = time.time()
    while True:
        sms_data = get_sms_list(token)
        messages = sms_data.get("data", [])
        if messages:
            filtered = [
                m for m in messages
                if m["to"] == from_number and get_message_time(m) >= datetime.now(timezone.utc) - timedelta(minutes=10)
            ]
            if filtered:
                latest = max(filtered, key=get_message_time)
                code = extract_verification_code(latest['smsContent'])
                if code:
                    return code

        if time.time() - start_time > timeout:
            break
        time.sleep(interval)
        print("haven't found any messages. retrying")

    return None


