#!/usr/bin/python

##################################################################

# alerts_email.py by Jeff Johnston <jj358mhz@gmail.com>
# Alerting script (Email) for Scanner Listeners
# THIS FILE: /usr/local/bin/alerts_email.py
# No Warranty is implied, promised or permitted.

##################################################################


import json
import os
import urllib2

feedId = ''  # ENTER YOUR BROADCASTIFY FEED ID HERE
username = ''  # ENTER YOUR BROADCASTIFY USERNAME HERE
password = ''  # ENTER YOUR BROADCASTIFY PASSWORD HERE
email = ''  # ENTER YOUR ALERT DESTINATION EMAIL HERE

# This threshold amount is the number of listeners that need to be exceeded before email alerts are sent out
alertThreshold = 20  # ENTER YOUR DESIRED ALERT LISTENER THRESHOLD HERE

alertSubject = "[YOUR CHANNEL NAME HERE] Broadcastify Alert"  # ENTER YOUR BROADCASTIFY FEED NAME HERE
alertBody = "Broadcastify listener threshold exceeded " + str(alertThreshold) + " listeners.  "
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
