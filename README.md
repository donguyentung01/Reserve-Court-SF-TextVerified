# reservePickleball

A Python script to reserve pickleball courts in San Francisco (https://www.rec.us/organizations/san-francisco-rec-park). 

## How to run

Build a Docker image
```
docker build -t pickleball .

```
Run Python main script through Docker image with arguments
```
docker run --rm pickleball -c "<Court>" -d "<Date>" -s "<sport, either pickleball or tennis>" -t "<time>" -e "<rec.us account>" -p "<rec.us password>" -n "<Twilio phone number>" -a "<Twilio AuthToken>" -i "Twilio SID"
```

