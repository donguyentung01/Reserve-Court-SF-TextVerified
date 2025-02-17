# reservePickleball

A Python script to reserve pickleball courts in [San Francisco](https://www.rec.us/organizations/san-francisco-rec-park). 

## Prerequisites

You need to have an existing account with [rec.us](https://www.rec.us/). As of Feb 2025, [rec.us](https://www.rec.us/) blocks virtual numbers (like those created on Twilio, e.g.), so you need to use a real phone number for the registration (as opposed to a virtual number like on Twilio). 

You also need to create a Twilio virtual number, so that you can set up a Shortcuts automation task on your registered iPhone number to forward the text verification code, which is required for every court reservation, to the Twilio number. The text on your Twilio number is then retrieved by the Python script.

Here is the Shortcuts automation task setup you need to do: 

<img src="https://github.com/user-attachments/assets/8fde10fe-5fa5-4a83-bd47-d518e33f162f" width="300" />
<img src="https://github.com/user-attachments/assets/f1a37212-3464-444f-85c8-91dc81f53ffe" width="300" />


## How to run

Build a Docker image
```
docker build -t pickleball .

```
Run Python main script through Docker image with arguments
```
docker run --rm pickleball -c "<Court>" -d "<Date>" -s "<sport, either pickleball or tennis>" -t "<time>" -e "<rec.us account>" -p "<rec.us password>" -n "<Twilio phone number>" -a "<Twilio AuthToken>" -i "<Twilio SID>"
```

