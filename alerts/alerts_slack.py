#!/usr/bin/env python3

# VERSION: 2.4.3

##################################################################

# alerts_slack.py by Jeff Johnston <jj358mhz@gmail.com>
# Alerting script (Slack) for Scanner Listeners
# THIS FILE: /usr/local/bin/alerts_slack.py
# No Warranty is implied, promised or permitted.

# Schedule a cronjob for every x minutes (5 min is a good value)
# crontab -e and paste the entry below
# */x * * * * /usr/local/bin/alerts_slack.py

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
import requests
import syslog

# The Broadcastify API endpoint URL ** DO NOT ALTER **
BROADCASTIFY_API_URL = 'https://api.broadcastify.com/owner/?a=feed&feedId='

# Enter the account data for your Broadcastify feed
FEED_ID = ''  # ENTER YOUR BROADCASTIFY FEED ID HERE
USERNAME = ''  # ENTER YOUR BROADCASTIFY USERNAME HERE
PASSWORD = ''  # ENTER YOUR BROADCASTIFY PASSWORD HERE

# This threshold amount is the number of listeners that need to be exceeded before Slack alerts are sent out
ALERT_THRESHOLD = 0  # ENTER YOUR DESIRED ALERT LISTENER THRESHOLD HERE

# The Slack endpoint URL
WEBHOOK_URL = ''  # ENTER SLACK WEBHOOK URL


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


def slack_post(slack_payload):
    """Posts the message to the Slack webhook"""
    global WEBHOOK_URL
    sp = requests.post(WEBHOOK_URL, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
    if sp.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {sp.status_code}, the response is: {sp.text}")
    syslog.syslog(syslog.LOG_ALERT, f"Request to Slack returned a {sp.status_code}, the response is: {sp.text}")
    return sp.status_code


def main():
    """Main executable"""
    global ALERT_THRESHOLD, FEED_ID
    # Parses the Broadcastify JSON response
    response = broadcastify_request()
    descr = response['Feed'][0]['descr']
    listeners = response['Feed'][0]['listeners']
    status = response['Feed'][0]['status']

    # Slack status message payloads
    slack_payload_feed_up = {
        "text": f"*{descr} Broadcastify Alert* :cop::fire:\n"
                f"Listener threshold *{ALERT_THRESHOLD}* exceeded, the number of listeners = *{listeners}*\n"
                f"Broadcastify status code is: {status} <healthy is 1, unhealthy is 0>\n"
                f"Listen to the feed here: <https://www.broadcastify.com/listen/feed/{FEED_ID}>\n"
                f"Manage the feed here: <https://www.broadcastify.com/manage/feed/{FEED_ID}>"
    }

    slack_payload_feed_down = {
        "text": f"*{descr} Broadcastify Alert* :ghost:\n"
                "*FEED IS DOWN*\n"
                f"Broadcastify status code is: {status} <healthy is 1, unhealthy is 0>\n"
                f"Manage the feed here: <https://www.broadcastify.com/manage/feed/{FEED_ID}>"
    }

    # Calls the Slack webhook for message POST'ing
    if not status:
        slack_post(slack_payload_feed_down)
        syslog.syslog(syslog.LOG_ALERT, "Feed is down")
    else:
        if listeners >= ALERT_THRESHOLD:
            slack_post(slack_payload_feed_up)
            syslog.syslog(syslog.LOG_INFO, f"Listener threshold {ALERT_THRESHOLD} exceeded,\n"
                                           f"the number of listeners = {listeners}, firing a Slack alert")


if __name__ == '__main__':
    main()
