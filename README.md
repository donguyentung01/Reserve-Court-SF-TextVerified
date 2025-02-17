# reservePickleball

A Python script to reserve pickleball courts in San Francisco (https://www.rec.us/organizations/san-francisco-rec-park). 

## How to run

Build a Docker image
```
docker build -t pickleball .

```
Run the docker image with arguments
```
docker run --rm pickleball -c "Dolores" -d "2025-02-18" -s "tennis" -t "4:00 PM" -e "<rec.us account>" -p "<rec.us password>" -n "<Twilio phone number>" -a "<Twilio AuthToken>" -i "Twilio SID"
```

