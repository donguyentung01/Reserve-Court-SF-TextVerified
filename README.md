# Reserve Court SF

A Python script to reserve tennis/pickleball courts in [San Francisco](https://www.rec.us/organizations/san-francisco-rec-park). 

## Prerequisites

You need to have an existing account with [rec.us](https://www.rec.us/). As of Feb 2025, [rec.us](https://www.rec.us/) blocks virtual numbers (like those created on Twilio, e.g.), so you need to use a real phone number for the registration (as opposed to a virtual number like on Twilio). 

You also need to create a Twilio virtual number, so that you can set up a Shortcuts automation task on your registered iPhone number to forward the text verification code, which is required for every court reservation, to the Twilio number. The text on your Twilio number is then retrieved by the Python script.

Here is the recommended Shortcuts automation task setup: 


<img src="https://github.com/user-attachments/assets/d5562b2e-7d19-40d6-802d-574830293341" width="300" />
<img src="https://github.com/user-attachments/assets/34a0cc39-f1df-4e55-81b3-fa006dbe8069" width="300" />


## How to run

Build a Docker image
```
docker build -t pickleball .

```
Run Python main script through Docker image with arguments
```
docker run --rm pickleball -c "<Court>" -d "<Date>" -s "<sport, either pickleball or tennis>" -t "<start_time>" -y <end_time> -e "<rec.us account>" -p "<rec.us password>" -n "<Twilio phone number>" -a "<Twilio AuthToken>" -i "<Twilio SID>" -r "<datetime to run script>" -m
```



