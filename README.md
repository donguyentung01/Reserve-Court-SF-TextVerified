# Reserve Court SF

A Python script to reserve tennis/pickleball courts in [San Francisco](https://www.rec.us/organizations/san-francisco-rec-park). 

## Background 

Tennis/pickleball court reservations in San Francisco are done online on [rec.us](https://www.rec.us/). 

<img width="1366" alt="Screenshot 2025-04-09 at 1 23 56 PM" src="https://github.com/user-attachments/assets/ffd2f69c-950d-4aed-8cb1-64ef0db61c90" />


Court registration is open at a specific time during the day. For example, Alice Marble courts are reservable 8 days in advance at exactly 8:00AM each day. 

There are 3 main issues with reserving the courts manually: 
- You have to click/navigate the website really fast as soon as the registration opens, since a lot of players will also try to reserve the same courts. Courts will usually be fully reserved within 5-10 seconds after opening.
- Court registration requires SMS mobile verification, which can take more time to reserve manually
<img width="552" alt="Screenshot 2025-04-09 at 1 25 24 PM" src="https://github.com/user-attachments/assets/aa29861b-c881-4488-b3a0-a47b44643700" />

- The court registration times are not always convenient. For example, Alice Marble's registration opens at 8:00 AM, which may be too early for some people.

## Project Goal 

The script should be able to: 
- Reserve a given court at a given timeslot. 
- Outperform non-scripting users in terms of runtime. Ideally also outperform other script users. 

## Prerequisites

You need to have an existing account with [rec.us](https://www.rec.us/) or create an account otherwise. Each account is associated with a phone number, as each registration requires SMS mobile verification. As of Feb 2025, [rec.us](https://www.rec.us/) blocks virtual numbers (like those created on Twilio, e.g.), so you need to use a non-VOIP number for your account. Do not use your personal number, as it can get difficult to integrate with the script. 

You should rent a phone number on [https://www.textverified.com/](TextVerified). You also need to have your API key (under the [https://www.textverified.com/app/api/configure](API) section). 

## How to run

Install dependencies 
```
pip3 install -r requirements.txt 
```

Run `main.py` script 

```
python3 main.py -c "<Court>" -d "<Date>" -s "<sport, either pickleball or tennis>" \
-t "<start_time>" -y <end_time> -e "<rec.us account>" -p "<rec.us password>" \
-n "<TextVerified phone number>" -u "<TextVerified username>" -a "<TextVerified API Key>" -r "<date/time when court registration opens>" -m
```

For example, let's say we want to reserve court Alice Marble from 6:00PM to 7:30PM on 2025-04-09. Alice Marble registration opens 7 days in advance at 8AM, which means the registration time is 8AM on 2025-04-02. Lastly, assume my account is john.doe@gmail.com, my password is 12345678, my TextVerified phone number is (484)-567-8901, my TextVerified username is john.doe@gmail.com. and my TextVerified API Key is 1234. Then I should run this command about 2 minutes before the registration opens (around 07:58:00 on 2025-04-02):

`python3 main.py -c "Alice Marble" -d 2025-04-09 -s tennis -t 18:00:00 -y 19:30:00 -e john.doe@gmail.com -p 12345678 -n 4845678901 -u john.doe@gmail.com -a 1234 -r "2025-04-02 08:00:00" -m`


## Implementation

- The script uses Selenium to open and log in to [rec.us](https://www.rec.us/) 2 minutes before the registration opens. Then it retrieves the access token from Cookies--the access token will be attached to all HTTP requests' headers later on. 

| !<img width="946" alt="Screenshot 2025-04-09 at 1 28 32 PM" src="https://github.com/user-attachments/assets/8f8ed1e1-3816-4407-93a6-9073630eb5b9" /> | 
|:--:| 
| *Access token stored in Cookies* |

- 1 minute before the registration opens, submit an HTTP request at https://api.rec.us/v1/users/mobile-totp/send to ask for a mobile verification code.
  
- The script makes a GET request to TextVerified SMS endpoint to find the verification code.

- As soon as the registration opens, submit an HTTP request at https://api.rec.us/v1/users/mobile-totp/verify with the verication code in the request body. 

- After confirming that the verification code is correct, submit an HTTP request at https://api.rec.us/v1/reservations with all the information about court, timeslot, etc in the request body. 

- If the returned response is OK, then we have successfully reserved the court.
  
| !<img width="551" alt="Screenshot 2025-04-09 at 1 48 32 PM" src="https://github.com/user-attachments/assets/a04f6086-059f-41b8-bcb1-a399d2aaf35d" /> | 
|:--:| 
| *Court reserved successfully* |

The script is currently deployed on AWS EC2 and scheduled to run daily right before court reservation opens, using the EC2 crontab. 

## Optimization 

### Use API instead of web-crawling
The original version of this script simply uses web-crawling with Selenium to reserve the courts. This means that the script navigates the website just like a human user. However, this results in many failed attempts at court reservation, since the script is not fast enough. 

Afterwards, I switched from web-crawling to directly using the website's APIs. This approach eliminates 5-6 seconds of runtime that were previously used for navigating/clicking buttons. 

### Request verification code preemptively
After experimenting with the verification code mechanism on [rec.us](https://www.rec.us/), I discovered that the verification code can remain valid for up to 2 minutes. So instead of waiting until the court opening to request the verification code, we can request it right before the court opening, so we can save some extra runtime during the actual reservation. 

### Sending requests to multiple courts concurrently 
Each main court usually has multiple sub-courts. For example, Alice Marble has 4 different tennis courts. Each of the court registration would require a separate HTTP request at https://api.rec.us/v1/reservations. 

The script used multi-threading to paralellize sending HTTP requests, optimizing the runtime of the reservation.

## Results 

### Court reservation success rate 

### Performance comparison between single-threading & multi-threading 

## Challenges during development

### Researching HTTP request 
There is no official documentation on how [rec.us](https://www.rec.us/) APIs work. So I had to manually inspect the network tab on my browser to figure out what HTTP endpoints are being used. 

One particular challenge is that all the HTTP request headers are sent with Authorization attribute set to "bearer <access_token>". This access token is stored in a session cookie, and has to be retrieved from the Cookies section after the user logs in. Without the access token, the requests will be invalidated. 

### Rec.us blocking virtual number
[rec.us](https://www.rec.us/) blocks virtual number, which means you have to get a non-VOIP number and set up a webhook to my Flask endpoint on an AWS EC2 instance, which can handle verification messages.



