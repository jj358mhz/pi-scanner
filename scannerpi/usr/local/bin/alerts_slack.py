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
import logging
import os
import requests

_LOGGER = logging.getLogger(__name__)

# The Broadcastify API endpoint URL ** DO NOT ALTER **
BROADCASTIFY_API_URL = 'https://api.broadcastify.com/owner/?a=feed&feedId='
BROADCASTIFY_LISTEN_URL = 'https://www.broadcastify.com/listen/feed/'
BROADCASTIFY_MANAGE_URL = 'https://www.broadcastify.com/manage/feed/'


# Enter the account data for your Broadcastify feed
FEED_ID = ''  # ENTER YOUR BROADCASTIFY FEED ID HERE
USERNAME = ''  # ENTER YOUR BROADCASTIFY USERNAME HERE
PASSWORD = ''  # ENTER YOUR BROADCASTIFY PASSWORD HERE

# This threshold amount is the number of listeners that need to be exceeded before Slack alerts are sent out
ALERT_THRESHOLD = 0  # ENTER YOUR DESIRED ALERT LISTENER THRESHOLD HERE

# The Slack endpoint URL
WEBHOOK_URL = ''  # ENTER SLACK WEBHOOK URL

path_to_log_file = '/var/scannerpi/logs/'  # absolute filepath
# Check whether the specified path exists
pathExist = os.path.exists(path_to_log_file)
if not pathExist:
    # Create the directory if it does not exist
    os.makedirs(path_to_log_file)
    print(f'[upl-py_PATH] ID3 log folder path does not exist, creating: {path_to_log_file}')


def broadcastify_request():
    """Fetches the response from the Broadcastify feed API"""
    global BROADCASTIFY_API_URL, FEED_ID, USERNAME, PASSWORD
    url = BROADCASTIFY_API_URL + FEED_ID + '&type=json&u=' + USERNAME + '&p=' + PASSWORD
    data = {}  # Sets empty data dictionary
    try:
        r = requests.get(url)
        data = r.json()
        _LOGGER.info(f"Broadcastify API endpoint healthy, response data is: {data}")
        # syslog.syslog(syslog.LOG_INFO, f"Broadcastify API endpoint healthy, response data is: {data}")
    except ConnectionError as error:
        _LOGGER.error(f"Broadcastify API endpoint returned error code {error}")
        # syslog.syslog(syslog.LOG_ALERT, f"Broadcastify API endpoint returned error code {error}")
    return data


def slack_post(slack_payload):
    """Posts the message to the Slack webhook"""
    global WEBHOOK_URL
    sp = requests.post(WEBHOOK_URL, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
    if sp.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {sp.status_code}, the response is: {sp.text}")
    _LOGGER.error(f"Request to Slack returned a {sp.status_code}, the response is: {sp.text}")
    # syslog.syslog(syslog.LOG_ALERT, f"Request to Slack returned a {sp.status_code}, the response is: {sp.text}")
    return sp.status_code


def main():
    """Main executable"""
    global ALERT_THRESHOLD, BROADCASTIFY_LISTEN_URL, BROADCASTIFY_MANAGE_URL, FEED_ID
    logging.basicConfig(
        filename='/var/scannerpi/logs/slack.log',
        format='%(asctime)s %(levelname)-5s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
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
                f"Listen to the feed here: <{BROADCASTIFY_LISTEN_URL}{FEED_ID}>\n"
                f"Manage the feed here: <{BROADCASTIFY_MANAGE_URL}{FEED_ID}>"
    }

    slack_payload_feed_down = {
        "text": f"*{descr} Broadcastify Alert* :ghost:\n"
                "*FEED IS DOWN*\n"
                f"Broadcastify status code is: {status} <healthy is 1, unhealthy is 0>\n"
                f"Manage the feed here: <{BROADCASTIFY_MANAGE_URL}{FEED_ID}>"
    }

    # Calls the Slack webhook for message POST
    if not status:
        slack_post(slack_payload_feed_down)
        _LOGGER.critical("Feed is down")
        # syslog.syslog(syslog.LOG_ALERT, "Feed is down")
    else:
        if listeners >= ALERT_THRESHOLD:
            slack_post(slack_payload_feed_up)
            _LOGGER.info(f"Listener threshold {ALERT_THRESHOLD} exceeded,\n"
                         f"the number of listeners = {listeners}, firing a Slack alert")


if __name__ == '__main__':
    main()
