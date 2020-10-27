#!/usr/bin/python3

# <bitbar.title>wfmr-tracker</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Edward</bitbar.author>
# <bitbar.author.github>0xedward</bitbar.author.github>
# <bitbar.desc>A BitBar plugin to track Wells Fargo's mortgage interest rates and sends you a txt notification with Twilio</bitbar.desc>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/0xedward/wfmr-bitbar</bitbar.abouturl>

import os
from os import path
import sys
import datetime

import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

"""SETUP - Change the values below"""
TWILIO_ACCOUNT_SID = 'INSERT YOUR ACCOUNT SID HERE' # TODO should store in env
TWILIO_AUTH_TOKEN = 'INSERT YOUR AUTH TOKEN HERE'  # TODO should store in env
TWILIO_PHONE_NUMBER = 'INSERT TWILIO NUMBER' # format phone numbers with country code +11111111111
YOUR_PHONE_NUMBER = 'INSERT YOUR PHONE NUMBER'
"""END SETUP"""

if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    home_dir = os.path.expanduser('~')
    os.chdir(home_dir)

    try:
        # open log 
        most_recent_rate = -1.0
        most_recent_pts = -1.0
        first_run = False if path.isfile('mortgage-interest-rates.log') else True

        if not first_run:
            with open('wfmr.log') as read_log:
                for line in read_log:
                    pass
                last_read_rate = line.split('|')[2].strip()
                most_recent_rate = float(last_read_rate[:len(last_read_rate)-1])
                most_recent_pts = float(line.split('|')[3].strip())

        with open("wfmr.log","a+") as output_log:
            # make request      
            wells_fargo = requests.get('https://www.wellsfargo.com/mortgage/rates/purchase-assumptions?prod=1')
            if wells_fargo.status_code == 200:
                # parse response
                parser = BeautifulSoup(wells_fargo.text, 'lxml')
                current_interest_rate = parser.find('td', {'headers':'productName intRate'}).text
                description = str(parser.findAll('p')[3])
                start_idx = description.index("includes") + 8
                end_idx = description.index("in <")
                current_discount_points = description[start_idx:end_idx].strip()
            else:
                raise Exception("Wells Fargo website is unavailable")
            
            # send notification if rate dropped
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            if not first_run and most_recent_rate != -1.0 and most_recent_pts != -1.0 and (most_recent_rate > float(current_interest_rate.strip("%")) or most_recent_pts > float(current_discount_points)):
                message = client.messages.create(
                    body="Wells Fargo 30yr Fixed Rate dropped from {old_rate}% {old_pts} pts to {new_rate} {new_pts} pts".format(old_rate=most_recent_rate, old_pts=most_recent_pts, new_rate=current_interest_rate, new_pts=current_discount_points),
                    from_=TWILIO_PHONE_NUMBER,
                    to=YOUR_PHONE_NUMBER)
                output_log.write("{time} | Wells Fargo 30yr Fixed | {rate} | {pts} | Twilio Notification Sent \n".format(time=current_time, rate=current_interest_rate, pts=current_discount_points));
            else:
                # write to log
                output_log.write("{time} | Wells Fargo 30yr Fixed | {rate} | {pts} \n".format(time=current_time, rate=current_interest_rate, pts=current_discount_points));
            print("{rate} at {pts} pts".format(rate=current_interest_rate, pts=current_discount_points))

    except:
        print("Last fetch failed")
        with open("wfmr-error.log","a+") as error_log:
            error_log.write("{time} | {err}\n".format(time=current_time, err=sys.exc_info()[1]))
