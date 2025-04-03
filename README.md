# Reserve Court SF

A Python script to reserve tennis/pickleball courts in [San Francisco](https://www.rec.us/organizations/san-francisco-rec-park). 

## Background 

Tennis/pickleball court reservations in San Francisco are done online on [rec.us](https://www.rec.us/). 

Court registration is open at a specific time during the day. For example, Alice Marble courts are reservable 8 days in advance at exactly 8:00AM each day. 

There are 2 main issues with reserving the courts manually: 
- You have to click/navigate the website really fast as soon as the registration opens, since a lot of players will also try to reserve the same courts. Courts will usually be fully reserved within 5-10 seconds after opening. 
- The court registration times are not always convenient. For example, Alice Marble's registration opens at 8:00 AM, which may be too early for some people.

## Project Goal 

The script should be able to: 
- Reserve a given court at a given timeslot. 
- Outperform non-scripting users in terms of runtime. Ideally also outperform other script users. 

## Implementation

The script uses Selenium to open and log in to [rec.us](https://www.rec.us/) 2 minutes before the registration opens. Then it retrieves the access token from Cookies--the access token will be attached to all HTTP requests' headers later on. 

1 minute before the registration opens, submit an HTTP request at https://api.rec.us/v1/users/mobile-totp/send to ask for a mobile verification code. This verification code lasts for 1 minute. The verification will then be forwarded from my personal number to my Twilio number. The script polls the Twilio number to see if there is any incoming message within the last minute. Retrieve the verification number if there is one. 

As soon as the registration opens, submit an HTTP request at https://api.rec.us/v1/users/mobile-totp/verify with the verication code in the request body. 

After confirming that the verification code is correct, submit an HTTP request at https://api.rec.us/v1/reservations with all the information about court, timeslot, etc in the request body. 

If the returned response is OK, then we have successfully reserved the court. 

The script is currently deployed on AWS EC2 and scheduled to run daily right before court reservation opens, using the EC2 crontab. 

## Optimization 

### Use API instead of web-crawling
The original version of this script simply uses web-crawling with Selenium to reserve the courts. This means that the script navigates the website just like a human user. However, this results in many failed attempts at court reservation, since the script is not fast enough. 

Afterwards, I switched from web-crawling to directly using the website's APIs. This approach eliminates 5-6 seconds of runtime that were previously used for navigating/clicking buttons. 

### Request verification code preemptively
After experimenting with the verification code mechanism on [rec.us](https://www.rec.us/), I discovered that the verification code can remain valid for up to 1 minute. So instead of waiting until the court opening to request the verification code, we can request it right before the court opening, so we can save some extra runtime during the actual reservation. 

### Sending requests to multiple courts concurrently 
Each main court usually has multiple sub-courts. For example, Alice Marble has 4 different tennis courts. Each of the court registration would require a separate HTTP request at https://api.rec.us/v1/reservations. 

The script used multi-threading to paralellize sending HTTP requests, optimizing the runtime of the reservation.

## Results 

### Court reservation success rate 

### Performance comparison between single-threading & multi-threading 

## Challenges during development

### Researching HTTP request 
There is no official documentation on how [rec.us](https://www.rec.us/) APIs work. So I had to manually inspect the network tab on my browser to figure out what HTTP endpoints are being used. 

One particular challenge is that all the HTTP request headers are sent with Authorization attribute set to "bearer <access_token>". This access token has to be retrieved from the Cookies. Without the access token, the requests will be invalidated. 

### Rec.us blocking virtual number
[rec.us](https://www.rec.us/) blocks virtual number, which means you cannot directly use a Twilio number for the script. I have to set up an Automation task on my personal phone to forward the verification code to my Twilio number. 

## Prerequisites

You need to have an existing account with [rec.us](https://www.rec.us/). As of Feb 2025, [rec.us](https://www.rec.us/) blocks virtual numbers (like those created on Twilio, e.g.), so you need to use a real phone number for the registration (as opposed to a virtual number like on Twilio). 

You also need to create a Twilio virtual number, so that you can set up a Shortcuts automation task on your registered iPhone number to forward the text verification code, which is required for every court reservation, to the Twilio number. The text on your Twilio number is then retrieved by the Python script.

Here is the recommended Shortcuts automation task setup: 


<img src="https://github.com/user-attachments/assets/d5562b2e-7d19-40d6-802d-574830293341" width="300" />
<img src="https://github.com/user-attachments/assets/34a0cc39-f1df-4e55-81b3-fa006dbe8069" width="300" />


## How to run

Install dependencies 
```
pip3 install -r requirements.txt 
```

Run main.py script 
```
python3 main.py -c "<Court>" -d "<Date>" -s "<sport, either pickleball or tennis>" -t "<start_time>" -y <end_time> -e "<rec.us account>" -p "<rec.us password>" -n "<Twilio phone number>" -a "<Twilio AuthToken>" -i "<Twilio SID>" -r "<datetime to run script>" -m
```


