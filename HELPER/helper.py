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
import sys  
import time as t
def spawn_driver(weblink): #create a web driver at the weblink provided 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = '/usr/bin/chromedriver' 
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options) 
    driver.get(weblink)
    return driver 

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
        WebDriverWait(driver, 10).until(
        lambda driver: len(driver.find_elements(By.XPATH, "//button[contains(text(),'Log In')]")) > 0
        )
        login = driver.find_elements(By.XPATH, "//button[contains(text(),'Log In')]")[0] 
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
        send_code = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Send Code')]"))
        )
        send_code.click()
    except Exception as e: 
        print(f"Error: {e}")
        print("Error: Failed at sending code step")
        sys.exit(1)

def verify_code(driver, code): 
    try:
        verification_code_input =  WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input"))
        )
        verification_code_input.send_keys(code) 

    except Exception as e: 
        print(f"Error: {e}")
        print("Error: Failed at code verification step")
        sys.exit(1)
        sys.exit(1)

def confirm(driver): 
    try: 
        confirm = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Confirm')]"))
        )
        confirm.click()
        done = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Done')]"))
        )
        done.click()
    except Exception as e: 
        print(f"Error: {e}")
        print("Error: Failed at confirmation step")
        sys.exit(1)

def book_court(court, date, sport, time, email, password, twilio_account_sid, twilio_auth_token, twilio_phone_number, slot): 
    sports_URL_code = {
        "pickleball": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "tennis": "bd745b6e-1dd6-43e2-a69f-06f094808a96"
    }

    driver = spawn_driver(f"https://www.rec.us/organizations/san-francisco-rec-park?tab=locations&date={date}&time={slot}&sports={sports_URL_code[sport]}")

    open_booking_court_time(driver, court, time) 
    log_in(driver, email, password)
    finalize_booking(driver) 
    send_code(driver) 
    verify_code(driver, get_code(twilio_account_sid, twilio_auth_token, twilio_phone_number))  
    confirm(driver)
    print(f"Successfully reserved court {court} at {time} on {date} for {sport}. Check for confirmation email at {email}")
    driver.quit()



