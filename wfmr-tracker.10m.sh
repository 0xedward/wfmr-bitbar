#!/bin/bash

# <bitbar.title>wfmr-tracker</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Edward</bitbar.author>
# <bitbar.author.github>0xedward</bitbar.author.github>
# <bitbar.desc>A BitBar plugin to track Wells Fargo's mortgage interest rates and sends you a txt notification with Twilio</bitbar.desc>
# <bitbar.abouturl>https://github.com/0xedward/wfmr-bitbar</bitbar.abouturl>

echo $(/usr/local/bin/python3 $(pwd)/wfmr-tracker/interest-rate-checker.py)