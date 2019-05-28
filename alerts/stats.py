#!/usr/bin/python

##################################################################

# stats.py by Jeff Johnston <jj358mhz@gmail.com>
# Allows email notification of broadcastify feed listeners
# THIS FILE: /usr/local/bin/stats.py
# No Warranty is implied, promised or permitted.

##################################################################

# The "mail" command above requires ssmtp & mailutils to be installed, see link below:
# https://raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails

##################################################################

# Add the following line to root's crontab (via sudo crontab -e):
#       */5 * * * * /usr/local/bin/stats.py
# This will purge an archive xx minutes after the top of every hour. You can update to suit your needs.

###################  >>> ENJOY !    ################################


import json
import os
import urllib2

# Feed access details
feedId = "put_your_radioreference_feedId_here"
feedTitle = "put_your_radioreference_feed_title_here"
username = "put_your_radioreference_username_here"
password = "put_your_radioreference_password_here"

#Notification destination email
email = "put_your_destination_email_here"

# Sets the listener alert threshold
alertThreshold = 30

alertSubject = feedTitle + " Broadcastify Alert"
alertBody = feedTitle + "Broadcastify listener threshold exceeded " + str(alertThreshold) + " listeners.  "
alertBody += "Listen to the feed here http://www.broadcastify.com/listen/feed/" + feedId + "  "
alertBody += "Manage the feed here http://www.broadcastify.com/manage/feed/" + feedId + "  "


url = "https://api.broadcastify.com/owner/?a=feed&feedId=" + feedId + "&type=json&u=" + username + "&p=" + password
response = urllib2.urlopen(url)
data = json.load(response)
listeners = data['Feed'][0]['listeners']
alertBody += "The current number of listeners is " + str(listeners) + "  "


if listeners > alertThreshold:
        cmd = 'echo ' + alertBody + ' | mail -s "' + alertSubject + '" ' + email
        os.system(cmd)
