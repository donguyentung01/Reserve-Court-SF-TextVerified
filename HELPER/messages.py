import requests
import time

def get_code(phone_number, webhook="http://54.183.149.104:5000/", timeout=30, poll_interval=1, max_age=60):
    """
    Polls the webhook for the verification code for a given phone number.

    :param phone_number: The phone number to search for in the webhook logs.
    :param webhook: The base URL of the webhook (default: "http://54.183.149.104:5000/").
    :param timeout: The maximum time to wait (in seconds) before giving up.
    :param poll_interval: The interval (in seconds) to wait between polling attempts.
    :param max_age: The maximum age of the record to look for (in seconds).
    :return: The verification code if found, or -1 if not found within the timeout.
    """
    
    start_time = time.time()  # Record the start time to track timeout
    
    while time.time() - start_time < timeout:
        try:
            # Build the request URL
            url = f"{webhook}get_verification_code?phonenumber={phone_number}&maxage={max_age}"
            response = requests.get(url, timeout=poll_interval)
            
            # If the request is successful and we get a valid response
            if response.status_code == 200:
                data = response.json()
                # If the response contains the verification code
                if 'verification_code' in data:
                    return data['verification_code']
        
        except requests.RequestException:
            pass  # Ignore exceptions and continue retrying
        
        # Wait for the specified poll interval before retrying
        time.sleep(poll_interval)
    
    # If no verification code is found within the timeout, return -1
    return -1
