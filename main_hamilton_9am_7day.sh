#!/bin/bash

#set up global variables 
COURT="Hamilton" 
SPORT="tennis"
START_TIME="09:00:00"
END_TIME="10:30:00" 
CURRENT_DATE=$(TZ="America/Los_Angeles" date +"%Y-%m-%d") 
TARGET_TIME="${CURRENT_DATE} 08:00:00"
RESERVATION_DATE=$(TZ="America/Los_Angeles" date -d "7 days" +"%Y-%m-%d")
EMAIL="qchinguyen01@gmail.com"
PASSWORD="tung2001"
PHONE_NUMBER="2182075868"
USERNAME="qchinguyen01@gmail.com"
APIKEY="nv51ovsEpNqaHTEkcAmvALiS3lkzohZuq1VHTYBIOmfQrn6yNhNBCRSWb7gfXEC"
#run PYTHON program to reserve courts

echo "Running the following command: python3 main.py -c "\"$COURT\"" -d "$RESERVATION_DATE" -s "$SPORT" -t "$START_TIME" -y "$END_TIME" \
-e "$EMAIL" -p "$PASSWORD" -n "$PHONE_NUMBER" -u "$USERNAME" -a "$APIKEY" \
-r "\"$TARGET_TIME\"" -m"

python3 main.py -c "$COURT" -d "$RESERVATION_DATE" -s "$SPORT" -t "$START_TIME" -y "$END_TIME" \
-e "$EMAIL" -p "$PASSWORD" -n "$PHONE_NUMBER" -u "$USERNAME" -a "$APIKEY" \
-r "$TARGET_TIME" -m   
