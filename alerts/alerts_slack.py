#!/usr/bin/env python3

# VERSION: 2.4.2

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
WEBHOOK_URL = ''  # ENTER YOUR SLACK WEBHOOK URL HERE

# Sets empty data dictionary
DATA = {}


def broadcastify_request():
    """Fetches the response from the Broadcastify feed API"""
    global BROADCASTIFY_API_URL, FEED_ID, USERNAME, PASSWORD, DATA
    url = BROADCASTIFY_API_URL + FEED_ID + '&type=json&u=' + USERNAME + '&p=' + PASSWORD
    try:
        r = requests.get(url)
        DATA = r.json()
        syslog.syslog(syslog.LOG_INFO, 'Broadcastify API endpoint healthy, response data is: {}'.format(DATA))
    except ConnectionError as error:
        syslog.syslog(syslog.LOG_ALERT, 'Broadcastify API endpoint returned error code {}'.format(error))
    return DATA


def slack_post(slack_payload):
    """Posts the message to the Slack webhook"""
    global WEBHOOK_URL
    sp = requests.post(WEBHOOK_URL, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
    if sp.status_code != 200:
        raise ValueError('Request to Slack returned an error %s, the response is:\n'
                         '%s' % (sp.status_code, sp.text))
    syslog.syslog(syslog.LOG_ALERT,
                  'Request to Slack returned a {}, the response is: {}'.format(sp.status_code, sp.text))
    return sp.status_code


def main():
    """Main executable"""
    global ALERT_THRESHOLD, FEED_ID
    # Parses the Broadcastify JSON response
    broadcastify_request()
    descr = DATA['Feed'][0]['descr']
    listeners = DATA['Feed'][0]['listeners']
    status = DATA['Feed'][0]['status']

    # Slack status message payloads
    slack_payload_feed_up = {
        "text": "*{} Broadcastify Alert* :cop::fire:\n"
                "Listener threshold *{}* exceeded, the number of listeners = *{}*\n"
                "Broadcastify status code is: {} <healthy is 1, unhealthy is 0>\n"
                "Listen to the feed here: <http://www.broadcastify.com/listen/feed/{}>\n"
                "Manage the feed here: <http://www.broadcastify.com/manage/feed/{}>".format(descr, ALERT_THRESHOLD,
                                                                                            listeners,
                                                                                            status,
                                                                                            FEED_ID,
                                                                                            FEED_ID)
    }

    slack_payload_feed_down = {
        "text": "*{} Broadcastify Alert* :ghost:\n"
                "*FEED IS DOWN*\n"
                "Broadcastify status code is: {} <healthy is 1, unhealthy is 0>\n"
                "Manage the feed here: <http://www.broadcastify.com/manage/feed/{}>".format(descr, status, FEED_ID)
    }

    # Calls the Slack webhook for message POST'ing
    if not status:
        slack_post(slack_payload_feed_down)
        syslog.syslog(syslog.LOG_ALERT, 'Feed is down')
    else:
        if listeners >= ALERT_THRESHOLD:
            slack_post(slack_payload_feed_up)
            syslog.syslog(syslog.LOG_INFO,
                          'Listener threshold {} exceeded, the number of listeners = {}, firing a Slack alert'.format(
                              ALERT_THRESHOLD, listeners))


if __name__ == '__main__':
    main()
