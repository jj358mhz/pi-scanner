#!/usr/bin/env python3

# VERSION: 2.4.0

##################################################################

# alerts_email.py by Jeff Johnston <jj358mhz@gmail.com>
# Alerting script (Email) for Scanner Listeners
# THIS FILE: /usr/local/bin/alerts_email.py
# No Warranty is implied, promised or permitted.

# Schedule a cronjob for every x minutes (5 min is a good value)
# crontab -e and paste the entry below
# */x * * * * /usr/local/bin/alerts_email.py

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

##################################################################


import json
import os
import urllib.request

feedID = ''  # ENTER YOUR BROADCASTIFY FEED ID HERE
username = ''  # ENTER YOUR BROADCASTIFY USERNAME HERE
password = ''  # ENTER YOUR BROADCASTIFY PASSWORD HERE
email = ''  # ENTER YOUR ALERT DESTINATION EMAIL HERE

# This threshold amount is the number of listeners that need to be exceeded before email alerts are sent out
alertThreshold = 20  # ENTER YOUR DESIRED ALERT LISTENER THRESHOLD HERE

url = "https://api.broadcastify.com/owner/?a=feed&feedId=" + feedID + "&type=json&u=" + username + "&p=" + password
response = urllib.request.urlopen(url)
data = json.load(response)
descr = data['Feed'][0]['descr']
listeners = data['Feed'][0]['listeners']

alertSubject = "{} Broadcastify Alert".format(descr)
alertBody = "Broadcastify listener threshold {} exceeded ".format(alertThreshold) + " listeners.  "
alertBody += "Listen to the feed here https://www.broadcastify.com/listen/feed/" + feedID + "  "
alertBody += "Manage the feed here https://www.broadcastify.com/manage/feed/" + feedID + "  "
alertBody += "The current number of listeners is {}".format(listeners) + "  "

if listeners > alertThreshold:
    cmd = 'echo ' + alertBody + ' | mail -s "' + alertSubject + '" ' + email
    os.system(cmd)
