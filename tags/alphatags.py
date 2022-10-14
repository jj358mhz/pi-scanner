#!/usr/bin/env python2

import time
from datetime import datetime

import requests
import serial

'''-----------------USER CONFIGURATION-----------------'''
# Tweaked slightly by mikewren@gmail.com, with better commenting and tag parsing and output
# See the technicals tab of your Broadcastify feed configuration page for the correct information to use below
port = "/dev/ttyACM0"  # Your scanner USB/serial port in quotes here - your RaspberryPi may be different
baudrate = 115200  # Your scanners baudrate here
icecastUser = "source"  # DO NOT enter your Broadcastify username, it must stay as source
icecastPass = "00000"  # Your Broadcastify password in quotes here
icecastServerAddress = "audio9.broadcastify.com:80"  # Your Broadcastify server IP Address (and port if necessary) here
icecastMountpoint = "00000"  # Your Broadcastify mountpoint in quotes here - don't add leading '/'
idleTimeLength = 30  # Number of seconds to wait to update an idle message
idleMessage = "Scanning..."  # The message to send to Broadcastify server when scanner is idle
'''-----------------END USER CONFIGURATION---------------'''
'''----------UNNECESSARY TO MODIFY SCRIPT BELOW----------'''

urlBase = "http://" + icecastServerAddress + "/admin/metadata?mount=/" + icecastMountpoint + "&mode=updinfo&song="
serTimeout = float(.005)  # serial timeout here (.005 is probably sufficient)
test = "GLG"  # '''test string to send to Uniden Scanner to get current status
# for BCT8 will be RF to get frequency, or LCD FRQ to read icon status
# for BC125AT use CIN'''
TGIDold = 0  # initialize TGID old test variable
metadata = ''
updateTime = datetime.now()

serialFromScanner = serial.Serial(port, baudrate, timeout=serTimeout)  # initialize serial connection
serialFromScanner.flushInput()  # flush serial input

serBuffer = ''  # clear the serBuffer
nextChar = ''  # reset the nextChar marker


def getData():
    global serBuffer, nextChar
    serialFromScanner.write(test + '\r\n')  # send initial request to scanner


def receiveData():
    if serialFromScanner.inWaiting() > 0:  # check to see if there's serial data waiting
        global nextChar, serBuffer
        while nextChar != '\r':  # continue filling serBuffer until carriage return
            nextChar = serialFromScanner.read(1)  # read one character
            serBuffer += nextChar


def parseData(pserBuffer):
    parsed = pserBuffer.split(",")
    stringtest = parsed[0]
    global TGIDold, TGID, metadata
    if stringtest == "GLG":
        length = len(parsed)
        if length >= 10:  # check list length so we don't get exception 10 for BCT15, 13 for BC886XT
            TGID = parsed[1]
            SYSNAME = parsed[5]
            GROUP = parsed[6]
            TG = parsed[7]
            FREQ = TGID.lstrip('0')  # remove leading 0 if present
            try:
                if FREQ[-1] == '0':  # remove trailing 0 if present
                    FREQ = FREQ[:-1]
            except Exception as e:
                print(e)
                pass

        if (TGID != TGIDold) and (TGID != ''):  # Check if group change or scanner not receiving
            # This is the alpha tag text that's sent to Broadcastify
            # metadata = ((FREQ) + " " + (SYSNAME) + " " + (GROUP) + " " + (TG))
            metadata = ((GROUP) + ": " + (TG) + " (" + (FREQ) + ")")
        else:
            metadata = ''


def updateData(pMetadata):
    global TGID, TGIDold, updateTime
    if pMetadata != '':
        print(pMetadata)
        TGIDold = TGID
        metadataFormatted = metadata.replace(" ", "+")  # add "+" instead of " " for icecast2
        requestToSend = (urlBase) + (metadataFormatted)
        r = requests.get((requestToSend), auth=(icecastUser, icecastPass))
        status = r.status_code
        updateTimeGMT = time.gmtime()
        timestamp = time.asctime(updateTimeGMT)
        print(timestamp)
        updateTime = datetime.now()

        if status == 200:
            print("Icecast Update OK")
        else:
            print("Icecast Update Error", status)

    else:  # Count the time since the last update and if 30 s update with a "Scanning" message
        idleTime = datetime.now()
        timeCheck = (idleTime - updateTime).seconds

        if timeCheck >= idleTimeLength:
            requestToSendScanning = urlBase + idleMessage
            r2 = requests.get(requestToSendScanning, auth=(icecastUser, icecastPass))
            status = r2.status_code
            updateTimeGMT = time.gmtime()  # get update time GMT for printing
            timestamp = time.asctime(updateTimeGMT)
            updateTime = datetime.now()  # reset update time for counter
            print(idleMessage)
            print(timestamp)

            if status == 200:
                print("Icecast Update OK")
            else:
                print("Icecast Update Error", status)


while True:  # infinite loop
    getData()

    receiveData()

    parseData(serBuffer)

    updateData(metadata)

    time.sleep(.1)  # pause
