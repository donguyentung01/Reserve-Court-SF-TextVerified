import argparse 
import sys 
from HELPER.helper import * 


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="A script that reserves pickleball courts in San Francisco, CA.") 

    parser.add_argument('-c', '--court', type=str, required=True, help="Court, e.g. Balboa") 
    parser.add_argument('-d', '--date', type=str, required=True, help="Date, e.g. 2025-01-10") 
    parser.add_argument('-s', '--sport', type=str, required=True, help="Sport, either pickleball or tennis") 
    parser.add_argument('-t', '--starttime', type=str, required=True, help = "Time, e.g. 09:00:00") 
    parser.add_argument('-y', '--endtime', type=str, required=True, help = "Time, e.g. 10:00:00") 
    parser.add_argument('-e', '--email', type=str, required=True, help="Your rec.us email")
    parser.add_argument('-p', '--password', type=str, required=True, help="Your rec.us password") 
    parser.add_argument('-n', '--phone', type=str, required=True, help="Twilio phone number")
    parser.add_argument('-r', '--targettime', type=str, required=True, help="Target time, e.g. 2025-03-30 12:00:00")
    parser.add_argument('-m', '--multithreaded', action='store_true', help="enable multithreading")

    args = parser.parse_args()

    court, start_time, end_time, email, password, phone_number, date, sport, target_time, is_multithreaded = (
        args.court, args.starttime, args.endtime, args.email, args.password, args.phone, args.date, args.sport, args.targettime, args.multithreaded
    )

    if sport not in ("pickleball", "tennis"): 
        print("Sport must be either 'pickleball' or 'tennis'") 
        sys.exit(1)

    book_court(court, date, sport, start_time, end_time, email, password, phone_number, is_multithreaded, target_time) 