#!/bin/bash

#set up global variables 
COURT="Lafayette" 
SPORT="tennis"
START_TIME="18:00:00"
END_TIME="19:00:00" 
CURRENT_DATE=$(TZ="America/Los_Angeles" date +"%Y-%m-%d") 
TARGET_TIME="${CURRENT_DATE} 12:00:00"
RESERVATION_DATE=$(TZ="America/Los_Angeles" date -d "2 days" +"%Y-%m-%d")
EMAIL="aramguess@gmail.com"
PASSWORD="tung2001"
PHONE_NUMBER="3206480672"
USERNAME="qchinguyen01@gmail.com"
APIKEY="nv51ovsEpNqaHTEkcAmvALiS3lkzohZuq1VHTYBIOmfQrn6yNhNBCRSWb7gfXEC"
#run PYTHON program to reserve courts

echo "Running the following command: python3 main.py -c "\"$COURT\"" -d "$RESERVATION_DATE" -s "$SPORT" -t "$START_TIME" -y "$END_TIME" \
-e "$EMAIL" -p "$PASSWORD" -n "$PHONE_NUMBER" -u "$USERNAME" -a "$APIKEY" \
-r "\"$TARGET_TIME\"" -m"

python3 main.py -c "$COURT" -d "$RESERVATION_DATE" -s "$SPORT" -t "$START_TIME" -y "$END_TIME" \
-e "$EMAIL" -p "$PASSWORD" -n "$PHONE_NUMBER" -u "$USERNAME" -a "$APIKEY" \
-r "$TARGET_TIME" -m   
