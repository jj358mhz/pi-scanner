#!/usr/bin/python

##################################################################

# stats_html.py by Jeff Johnston <jj358mhz@gmail.com>
# Allows email notification of broadcastify feed listeners
# THIS FILE: /usr/local/bin/stats_html.py
# No Warranty is implied, promised or permitted.

##################################################################

# The "mail" command above requires ssmtp & mailutils to be installed, see link below:
# https://raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails

##################################################################

# Add the following line to root's crontab (via sudo crontab -e):
#       */5 * * * * /usr/local/bin/stats_html.py
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

alertSubject = str(feedTitle) + " Broadcastify Alert"
alertBody = str(feedTitle) + <p>"Broadcastify listener threshold exceeded " + str(alertThreshold) + " listeners</p>."
alertBody += "<p><a href='http://www.broadcastify.com/listen/feed/" + feedId + "'>Listen to the feed here</a></p>"
alertBody += "<p><a href='http://www.broadcastify.com/manage/feed/" + feedId + "'>Manage the feed here</a></p>"

url = "https://api.broadcastify.com/owner/?a=feed&feedId=" + feedId + "&type=json&u=" + username + "&p=" + password
response = urllib2.urlopen(url)
data = json.load(response)
listeners = data['Feed'][0]['listeners']
alertBody = "<h2>Current Listeners:  " + str(listeners) + "</h2>" + alertBody

if listeners > alertThreshold:
	cmd = 'echo ' + repr(alertBody) + ' | mail -a "Content-type: text/html;" -s "' + alertSubject + '" ' + email
	os.system(cmd)
