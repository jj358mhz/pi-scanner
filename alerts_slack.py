#!/usr/bin/python

##################################################################

# alerts_slack.py by Jeff Johnston <jj358mhz@gmail.com>
# Alerting script (Slack) for Scanner Listeners
# THIS FILE: /usr/local/bin/alerts_slack.py
# No Warranty is implied, promised or permitted.

##################################################################


import json
import requests
import urllib2

# The Broadcastify endpoint URL ** DO NOT ALTER **
broadcastifyURL = 'https://api.broadcastify.com/owner/?a=feed&feedId='

# Enter the account data for your Broadcastify feed
feedName = ''  # ENTER YOUR BROADCASTIFY FEED NAME HERE
feedID = ''  # ENTER YOUR BROADCASTIFY FEED ID HERE
username = ''  # ENTER YOUR BROADCASTIFY USERNAME HERE
password = ''  # ENTER YOUR BROADCASTIFY PASSWORD HERE

# This threshold amount is the number of listeners that need to be exceeded before Slack alerts are sent out
alertThreshold = 20  # ENTER YOUR DESIRED ALERT LISTENER THRESHOLD HERE

# The Slack endpoint URL
webhook_url = ''  # ENTER YOUR SLACK WEBHOOK URL HERE

url = broadcastifyURL + feedID + '&type=json&u=' + username + '&p=' + password
response = urllib2.urlopen(url)
data = json.load(response)
listeners = data['Feed'][0]['listeners']

slack_payload = {"text": "*[{}] Broadcastify Alert* :ghost:\n"
                         "Listener threshold *{}* exceeded. Listeners = *{}*\n"
                         "\n"
                         "Listen to the feed here: <http://www.broadcastify.com/listen/feed/{}>\n"
                         "Manage the feed here: <http://www.broadcastify.com/manage/feed/{}>".format(feedName,
                                                                                                     alertThreshold,
                                                                                                     listeners, feedID,
                                                                                                     feedID)}


def slack_alert(slack_payload, webhook_url):
    response = requests.post(webhook_url, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        raise ValueError(
            'Request to Slack returned an error %s, the response is:\n'
            '%s' % (response.status_code, response.text))


if listeners > alertThreshold:
    slack_alert(slack_payload, webhook_url)
