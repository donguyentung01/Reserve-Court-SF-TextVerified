# reservePickleball

A Python script to reserve pickleball courts in San Francisco (https://www.rec.us/organizations/san-francisco-rec-park). 

## How to run
```
docker build -t pickleball .

```

```
docker run --rm pickleball -c "Dolores" -d "2025-02-18" -s "tennis" -t "4:00 PM" -e "<rec.us account>" -p "<rec.us password>" -n "<Twilio phone number>" -a "<Twilio AuthToken>" -i "Twilio SID"
```

