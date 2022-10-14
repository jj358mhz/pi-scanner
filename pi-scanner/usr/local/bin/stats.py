#!/usr/bin/env python3

# VERSION: 2.4.0

##################################################################

# stats.py by Jeff Johnston <jj358mhz@gmail.com>
# Allows email notification of broadcastify feed listeners
# THIS FILE: /usr/local/bin/stats.py
# No Warranty is implied, promised or permitted.

##################################################################

# The "mail" command above requires ssmtp & mailutils to be installed, see link below:
# https://raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails

##################################################################

# Schedule a cronjob for every x minutes (5 min is a good value)
# crontab -e and paste the entry below
# */x * * * * /usr/local/bin/stats.py

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

# Feed access details
feedId = "put_your_radioreference_feedId_here"
feedTitle = "put_your_radioreference_feed_title_here"
username = "put_your_radioreference_username_here"
password = "put_your_radioreference_password_here"

# Notification destination email
email = "put_your_destination_email_here"

# Sets the listener alert threshold
alertThreshold = 30

alertSubject = feedTitle + " Broadcastify Alert"
alertBody = feedTitle + "Broadcastify listener threshold exceeded " + str(alertThreshold) + " listeners.  "
alertBody += "Listen to the feed here http://www.broadcastify.com/listen/feed/" + feedId + "  "
alertBody += "Manage the feed here http://www.broadcastify.com/manage/feed/" + feedId + "  "

url = "https://api.broadcastify.com/owner/?a=feed&feedId=" + feedId + "&type=json&u=" + username + "&p=" + password
response = urllib.request.urlopen(url)
data = json.load(response)
listeners = data['Feed'][0]['listeners']
alertBody += "The current number of listeners is " + str(listeners) + "  "

if listeners > alertThreshold:
    cmd = 'echo ' + alertBody + ' | mail -s "' + alertSubject + '" ' + email
    os.system(cmd)
