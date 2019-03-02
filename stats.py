#!/usr/bin/python


##################################################################

# stats.py by Jeff Johnston <jj358mhz@gmail.com>
# Alerting script for Scanner Listeners
# THIS FILE: /usr/local/bin/stats.py
# No Warranty is implied, promised or permitted.

##################################################################


import json
import os
import urllib2

feedId = ''
username = ''
password = ''
email = ''

alertThreshold = 5
alertSubject = "[UC Berkeley Police] Broadcastify Alert"
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

