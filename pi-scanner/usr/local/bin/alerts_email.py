#!/usr/bin/env python3

# VERSION: 2.4.3

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
import requests
import syslog

# The Broadcastify API endpoint URL ** DO NOT ALTER **
BROADCASTIFY_API_URL = 'https://api.broadcastify.com/owner/?a=feed&feedId='

# Enter the account data for your Broadcastify feed
FEED_ID = ''  # ENTER YOUR BROADCASTIFY FEED ID HERE
USERNAME = ''  # ENTER YOUR BROADCASTIFY USERNAME HERE
PASSWORD = ''  # ENTER YOUR BROADCASTIFY PASSWORD HERE
EMAIL = ''  # ENTER YOUR ALERT DESTINATION EMAIL HERE

# This threshold amount is the number of listeners that need to be exceeded before email alerts are sent out
ALERT_THRESHOLD = 0  # ENTER YOUR DESIRED ALERT LISTENER THRESHOLD HERE


def broadcastify_request():
    """Fetches the response from the Broadcastify feed API"""
    global BROADCASTIFY_API_URL, FEED_ID, USERNAME, PASSWORD
    url = BROADCASTIFY_API_URL + FEED_ID + '&type=json&u=' + USERNAME + '&p=' + PASSWORD
    data = {}  # Sets empty data dictionary
    try:
        r = requests.get(url)
        data = r.json()
        syslog.syslog(syslog.LOG_INFO, f"Broadcastify API endpoint healthy, response data is: {data}")
    except ConnectionError as error:
        syslog.syslog(syslog.LOG_ALERT, f"Broadcastify API endpoint returned error code {error}")
    return data


def main():
    """Main executable"""
    global ALERT_THRESHOLD, FEED_ID
    # Parses the Broadcastify JSON response
    response = broadcastify_request()
    descr = response['Feed'][0]['descr']
    listeners = response['Feed'][0]['listeners']

    alertSubject = f"{descr} Broadcastify Alert"
    alertBody = f"Broadcastify listener threshold {ALERT_THRESHOLD} exceeded " + " listeners.  "
    alertBody += "Listen to the feed here https://www.broadcastify.com/listen/feed/" + FEED_ID + "  "
    alertBody += "Manage the feed here https://www.broadcastify.com/manage/feed/" + FEED_ID + "  "
    alertBody += "The current number of listeners is {}".format(listeners) + "  "

    if listeners > ALERT_THRESHOLD:
        cmd = 'echo ' + alertBody + ' | mail -s "' + alertSubject + '" ' + EMAIL
        os.system(cmd)


if __name__ == '__main__':
    main()
