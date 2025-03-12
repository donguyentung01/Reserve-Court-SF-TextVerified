from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from HELPER.messages import get_code
from datetime import datetime, timedelta
import sys  
import time as t
import requests
import json

def wait_for_target_time(target_timestamp, sleep_itvl=0.1):
    #target_timestamp = "2025-03-05 5:40:00"
    print(f"waiting for target time: {target_timestamp}")
    target_time = datetime.strptime(target_timestamp, "%Y-%m-%d %H:%M:%S")
    while datetime.now() < target_time:
        time_to_wait = (target_time - datetime.now()).total_seconds()
        if time_to_wait > 0:
            t.sleep(min(time_to_wait, sleep_itvl))  # Sleep in small increments

def spawn_driver(weblink): #create a web driver at the weblink provided 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = '/usr/bin/chromedriver' 
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options) 
    driver.get(weblink)
    return driver 

def make_verification_request(verification_code, headers, url="https://api.rec.us/v1/users/mobile-totp/verify"): 
    print(f"sending back verification code {verification_code}")

    body = {
        "code": str(verification_code)
    }
    
    try:
        # Send the POST request with the body
        response = requests.post(url, headers=headers, data=json.dumps(body))
        
        if response.status_code == 200:
            return response.text # Assuming the response is in JSON format
        
        else:
            return f"Failed to make request. Status code: {response.status_code}. Response text: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
def make_reservation_request(headers, courtSportId, participantUserId, date, start_time, end_time, url="https://api.rec.us/v1/reservations"):
    # Define the body (data) for the POST request
    body = {
        "courtSportIds": [courtSportId],
        "from": {"date": date, "time": start_time},
        "participantUserId": participantUserId,
        "to": {"date": date, "time": end_time}
    }
    
    try:
        # Send the POST request with the body
        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json() # Assuming the response is in JSON format
        
        else:
            return f"Failed to make request. Status code: {response.status_code}. Response text: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_access_token(driver):
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'access_token':
            access_token = cookie['value']
            return access_token
    return None 

def getHeaders(driver):
    access_token = get_access_token(driver)
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Origin': 'https://www.rec.us',
            'Referer': 'https://www.rec.us/',
            "Content-Type": "application/json"
        }
        return headers 
    else:
        return None 

def make_send_verification_code_request(headers, url="https://api.rec.us/v1/users/mobile-totp/send"):
    print("requesting verification code") 
    # Define the body (data) for the POST request
    try:
        # Send the POST request with the body
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.text # Assuming the response is in JSON format
        
        else:
            return f"Failed to make request. Status code: {response.status_code}. Response text: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
def make_payment_request(url, headers):
    # Define the body (data) for the POST request
    body = {
        "data": {}
    }

    try:
        # Send the POST request with the body
        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json() # Assuming the response is in JSON format
        
        else:
            return f"Failed to make request. Status code: {response.status_code}. Response text: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
def get_verification_code_preemptively_day(driver, twilio_account_sid, twilio_auth_token, twilio_phone_number, current_date): 
    print(f"Getting verification code preemptively on {current_date}")
    driver.get(f'https://www.rec.us/organizations/san-francisco-rec-park?tab=locations&date={current_date}')

    try:
    # Wait until the paragraph with time is visible
        potential_timeslot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'0 AM') or contains(text(),'0 PM')]"))   
        )
        potential_timeslot.click()
        finalize_booking(driver) 
        send_code(driver) 
        verification_code = get_code(twilio_account_sid, twilio_auth_token, twilio_phone_number)
        if verification_code != -1:
            return verification_code
        return -1
    except Exception as e:
        print(e)
        return -1 

def get_verification_code_preemptively_multiday(driver, twilio_account_sid, twilio_auth_token, twilio_phone_number, start_date=datetime.today().strftime("%Y-%m-%d"), number_of_days=7):
    print("Getting verification code preemptively")
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

# Loop through the next 7 days including today
    for i in range(number_of_days):
        day = start_date_obj + timedelta(days=i)
        day_string = day.strftime("%Y-%m-%d")
        verification_code = get_verification_code_preemptively_day(driver, twilio_account_sid, twilio_auth_token, twilio_phone_number, day_string)
        if verification_code != -1:
            return verification_code

    return -1 

def open_booking_court_time(driver, court, time): 
    try:
        WebDriverWait(driver, 10).until(
            lambda driver: len(driver.find_elements(By.XPATH, f"//p[contains(text(),'{court}')]/ancestor::div[4]")) > 0 
        )
        ancestor_element = driver.find_element(By.XPATH, f"//p[contains(text(),'{court}')]/ancestor::*[4]") 
        button = ancestor_element.find_element(By.XPATH, f".//button[p[starts-with(text(),'{time}')]]")
        driver.execute_script("arguments[0].click();", button)

        WebDriverWait(driver, 10).until(
            lambda driver: len(driver.find_elements(By.XPATH, "//button[contains(text(),'Book')]")) > 0
        )
        book = driver.find_elements(By.XPATH, "//button[contains(text(),'Book')]")[0]
        book.click()
    except Exception as e:
        print(f"Error: {e}")
        print("Error: Failed at opening booking at court/time")
        sys.exit(1)

def log_in(driver, email, password): 
    try:
        print("Logging in")
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Log In')]")))
        login.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )

        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
    
        email_input.send_keys(email)  # Replace with your email
        password_input.send_keys(password)       # Replace with your password
    
        password_input.send_keys(Keys.RETURN)  # Alternatively, use .submit() on the form

    except Exception as e:
        print(f"Error: {e}")
        print("Error: Failed at login")
        sys.exit(1)

def finalize_booking(driver): 
    try: 
        print("Open booking information, e.g. participant, court, etc")
        p = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//p[text()='Select participant']"))
        )
        p.click()

        account_owner = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//small[text()='Account Owner']"))
        )

        account_owner.click()
        book = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Book')]"))
        )
        
        book.click()
    except Exception as e: 
        print(f"Error: {e}")
        print("Error: Failed at finalizing booking")
        sys.exit(1)

def send_code(driver): 
    try: 
        print("Asking for confirmation code")
        send_code = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Send Code')]"))
        )
        send_code.click()
    except Exception as e: 
        print(f"Error: {e}")
        print("Error: Failed at sending code step")
        sys.exit(1)

def get_court_href(driver, court):
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, f"//a[p[text()='{court}']]")
        )
    )

    href_link = element.get_attribute("href")

    return href_link

def make_get_court_info_request(url):
    response = requests.get(url)

# Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None 

def get_court_sport_id(response, sport_code):
    court_ids = []
    for court in response["location"]["courts"]:
        if court["sports"][0]["sportId"] == sport_code:
            court_ids.append(court["sports"][0]["id"])
    return court_ids

def make_user_profile_request(headers, url="https://api.rec.us/v1/users/household-members"):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None 

def book_court(court, date, sport, start_time, end_time, email, password, twilio_account_sid, twilio_auth_token, twilio_phone_number, slot, target_time=f"{datetime.today().strftime('%Y-%m-%d')} 12:00:00"): 
    sports_URL_code = {
        "pickleball": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "tennis": "bd745b6e-1dd6-43e2-a69f-06f094808a96"
    }
    
    driver = spawn_driver(f"https://www.rec.us/organizations/san-francisco-rec-park?tab=locations&date={date}&time={slot}&sports={sports_URL_code[sport]}")

    log_in(driver, email, password)
    t.sleep(2)
    headers = getHeaders(driver) 

    court_info_api_endpoint = f"https://api.rec.us/v1/{get_court_href(driver, court)[19:]}"
    all_court_data = make_get_court_info_request(court_info_api_endpoint)
    all_court_ids = get_court_sport_id(all_court_data, sports_URL_code[sport])

    user_data = make_user_profile_request(headers)
    user_id = user_data[0]['id']

    preemptive_verification_code_target_time_obj = datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=1)
    preemptive_verification_code_target_time = preemptive_verification_code_target_time_obj.strftime("%Y-%m-%d %H:%M:%S")

    wait_for_target_time(preemptive_verification_code_target_time) 

    make_send_verification_code_request(headers)
    verification_code = get_code(twilio_account_sid, twilio_auth_token, twilio_phone_number) 

    wait_for_target_time(target_time)    
    job_begin_time = t.time()
    make_verification_request(verification_code, headers)
    for court_id in all_court_ids:
        response = make_reservation_request(headers, court_id, user_id, date, start_time, end_time)
        if "order" in response: 
            order_id = response["order"]["id"]
            payment_status = make_payment_request(f"https://api.rec.us/v1/orders/{order_id}/pay", headers)
            if payment_status["data"]["status"] == "succeeded":
                print(f"Successfully reserve court {court} from {start_time} to {end_time}")
                job_end_time = t.time()
                print(f"Reservation job takes {job_end_time - job_begin_time} seconds.")
                sys.exit(0)
    print(f"Couldn't reserve the court")


    #t.sleep(1)
    #preemptive_verification_code_target_time_obj = datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=1)
    #preemptive_verification_code_target_time = preemptive_verification_code_target_time_obj.strftime("%Y-%m-%d %H:%M:%S")

    #wait_for_target_time(preemptive_verification_code_target_time) # wait for 1 minute before court opens to get verification code preemptively
    #preemptive_verification_code = get_verification_code_preemptively_multiday(driver, twilio_account_sid, twilio_auth_token, twilio_phone_number)

    #headers = getHeaders(driver) 
    #print(headers)
    #print(make_send_verification_code_request(headers))
    #verification_code = get_code(twilio_account_sid, twilio_auth_token, twilio_phone_number) 
    #print(make_verification_request(verification_code, headers))
    #response = make_reservation_request(headers)
    #print(response)
    #order_id = response["order"]["id"]
    #print(make_payment_request(f"https://api.rec.us/v1/orders/{order_id}/pay", headers))

    #preemptive_verification_code = get_verification_code_preemptively_multiday(driver, twilio_account_sid, twilio_auth_token, twilio_phone_number)
    #print(f"Successfully got verification code preemptively: {preemptive_verification_code}")

    #wait_for_target_time(target_time)
    #driver.get(f"https://www.rec.us/organizations/san-francisco-rec-park?tab=locations&date={date}&time={slot}&sports={sports_URL_code[sport]}")
    #make_verification_request(driver, "https://api.rec.us/v1/users/mobile-totp/verify", preemptive_verification_code)
    #response = make_reservation_request(driver, "https://api.rec.us/v1/reservations")
    #order_id = response["order"]["id"]
    #print(make_payment_request(driver, f"https://api.rec.us/v1/orders/{order_id}/pay"))

    #print(f"Successfully reserved court {court} at {time} on {date} for {sport}. Check for confirmation email at {email}")
    driver.quit()



