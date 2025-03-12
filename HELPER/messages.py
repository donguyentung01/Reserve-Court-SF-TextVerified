
import time
from twilio.rest import Client
from datetime import datetime, timezone

def get_code(account_sid, auth_token, phone_number, timeout=30, poll_interval=1, max_age_seconds=60):
    """
    Fetches the most recent verification code sent to the given phone number that was received
    within the last max_age_seconds
    
    Parameters:
    - account_sid: Twilio Account SID
    - auth_token: Twilio Auth Token
    - phone_number: Phone number to check for messages
    - timeout: Maximum time to wait for a message (in seconds)
    - poll_interval: Interval between each polling attempt (in seconds)
    - max_age_seconds: Maximum age of the message in seconds (default is 60 seconds)
    
    Returns:
    - latest_message.body: The body of the most recent message received within the specified time
    """

    client = Client(account_sid, auth_token)

    # Time when we start polling
    start_time = time.time()

    while True:
        # Fetch the most recent SMS message
        messages = client.messages.list(to=phone_number, limit=1)  # limit=1 fetches the most recent message
        
        # If we have found a message, check if it was received within the last `max_age_seconds`
        if messages:
            latest_message = messages[0]
            message_sent_time = latest_message.date_sent

            current_time = datetime.utcnow().replace(tzinfo=timezone.utc) 

            # Check if the message was sent within the last `max_age_seconds`
            if message_sent_time and (current_time - message_sent_time).total_seconds() <= max_age_seconds:
                return latest_message.body
        
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached. No valid message received within the specified time frame.")
            return -1  
        
        # Wait for the specified polling interval before checking again
        time.sleep(poll_interval)

