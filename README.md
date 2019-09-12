scannerpi
=========

scannerpi is a collection of scripts and configuration files that you can use to assist in setting up a RaspBerry Pi for streaming scanner audio to websites such as Broadcastify.com

# Step 1: RaspberryPi Pre-Configuration Steps

* These instructions assume you have installed Raspbian Buster on your Pi

## Audio set-up

* With your USB sound stick installed, in a terminal on the RasPi run the command 

```bash
arecord –l
```
and note the output. You should see something like this:

```bash
**** List of CAPTURE Hardware Devices ****
card 1: Device [Generic USB Audio Device], device 0: USB Audio [USB Audio]
Subdevices: 1/1
Subdevice #0: subdevice #0
```
* This indicates that the capture (recording) device is card one. The numbering starts at zero and the on-board audio on the RasPi is card 0 (but it does not have a capture device). In ALSA configuration it is referred to by device and sub-device thusly: “hw:1,0”.

Next connect speakers to the audio jack on the RasPi (not the USB output) and a microphone or other audio input to the USB sound stick. A scanner tuned to NOAA weather with continuous output works well. Adjust the volume to mid level if using a scanner, etc. Then enter:

```bash
arecord -D plughw:1,0 temp.wav 
```
* In this case we use the plug-in called "plug" to handle format conversion. Otherwise you could use “arecord –D hw:1,0 somefile.wav but you would need to explicitly set the format to match your sound stick. Using “plughw:1,0” makes life easier.

If using a microphone, speak into it for about ten seconds. Then type “ctl-c” to stop recording. If you hear the audio when you enter the command,

```bash
aplay temp.wav
```
then the recording on the RasPi and USB device is working. If you don’t hear anything using “aplay temp.wav”, or if it is too soft or distorted, try using the command:

```bash
sudo alsamixer
```
(along with the volume control on the radio) to balance the recording level. After entering “alsamixer” press “F6” and select the sound card (maybe called generic USB device), then “F5” to display all controls for that device. 

Using one scanner I had to turn the scanner up quite loud, then using alsamixer turn on Auto Gain (arrow over to auto gain and press “**m**” until “**00**” is displayed). Using a different scanner I had to keep it rather low and turn auto gain off (mute) while keeping the capture level at + 9 dB - it’s fair to say “your mileage may vary.”

If despite all this you cannot get decent quality audio then you should suspect a problem with the attached audio hardware, audio cable, etc.

Once you have a feed running with good audio level you can save the alsamixer settings between reboots by issuing command:

```bash
sudo alsactl store
```

## Updates the Pi's Catalog, Kernel, & Firmware
Run these commands is successive order
```bash
sudo apt-get update
(wait)
```
```bash
sudo apt-get upgrade
(wait)
(reboot)
```
```bash
sudo rpi-update
(reboot)
```
# Step 2: Install Darkice & its Dependencies
This installs the Darkice package and its dependencies for file trimming and processing
```bash
sudo apt-get install darkice
```

## Install the SoX (Sound Exchange) & id3v2 Tag Packages
This command installs the *sox* package required for mp3 encoding
```bash
sudo apt-get install sox libsox-fmt-mp3 id3v2 -y
```

# Step 3: Configure & Install Support Scripts
This step will focus on installing and configuring DarkIce & Radioplay

## Folder Creation for Radioplay
```bash
sudo mkdir /etc/radioplay
sudo mkdir /var/lib/radioplay
sudo mkdir scanneraudio
```

## Download all Configurations Files
```bash
curl "https://raw.githubusercontent.com/jj358mhz/scannerpi/master/darkice.service" -o darkice.service && curl "https://raw.githubusercontent.com/jj358mhz/scannerpi/master/darkice.cfg" -o darkice.cfg && curl "https://raw.githubusercontent.com/jj358mhz/scannerpi/master/radioplay" -o radioplay && curl "https://raw.githubusercontent.com/jj358mhz/scannerpi/master/radioplay.conf" -o radioplay.conf

OR clone the repo

git clone https://github.com/jj358mhz/scannerpi.git
```
* **Update the *darkice.cfg* and *radioplay.conf* configuration files using vi or nano to conform it to your radioreference.com settings**
* **You may also need to modify the *radioplay* script at the *trim* area to customize the feed mnemonic**

### Edit Permission & Ownership
```bash
sudo chown root:root darkice darkice.cfg radioplay radioplay.conf
sudo chmod 755 radioplay darkice.service
sudo chmod 644 radioplay.conf darkice.cfg
```

### Move Files to Destination Folders
```bash
sudo mv radioplay /usr/local/bin/radioplay
sudo mv radioplay.conf /etc/radioplay/radioplay.conf
sudo mv darkice.service /etc/systemd/system/darkice.service
sudo mv darkice.cfg /etc/darkice.cfg
```

## Step 4: Test and Final Cleanup
Test DarkIce without archiving
```bash
sudo /usr/bin/darkice
```
Listen to the feed and adjust the levels as needed. If all works as expected then “ctl-c” to stop DarkIce. If you see this error when running DarkIce, “…lame lib opening underlying sink error…” then DarkIce was unable to connect to the server. Check “/etc/darkice.cfg” for the proper entries and make sure the RasPi can access the internet.

### Finalize the Installation
Update the root's crontab
```bash
sudo crontab -e
```
...and add the following lines
```bash
00 * * * *   [ -x /usr/local/bin/radioplay ] && /usr/local/bin/radioplay cron > /dev/null
```
Enable the DarkIce startup service to run at boot & start DarkIce
```bash
sudo systemctl enable darkice.service
sudo systemctl start darkice.service
```

## Reboot!

There is a live working feed accessible here <http://www.jj358mhz.com>

## Step 5: (OPTIONAL)

### Dropbox Uploader (third-party download)

<https://github.com/andreafabrizi/Dropbox-Uploader>

Dropbox Uploader is a BASH script which can be used to upload, download, delete, list files (and more!) from Dropbox, an online file sharing, synchronization and backup service.

It's written in BASH scripting language and only needs cURL.

Why use this script?

Portable: It's written in BASH scripting and only needs cURL (curl is a tool to transfer data from or to a server, available for all operating systems and installed by default in many linux distributions).
Secure: It's not required to provide your username/password to this script, because it uses the official Dropbox API for the authentication process.
Please refer to the <Wiki>(https://github.com/andreafabrizi/Dropbox-Uploader/wiki) for tips and additional information about this project. The Wiki is also the place where you can share your scripts and examples related to Dropbox Uploader.

### Dropbox Purge (dbpurge)

Dropbox purge (dbpurge) is an independent script that allows the user to purge their Dropbox app folder of the oldest archive recording. The script runs as a cron job (user-defined scheduling) and periodically deletes the oldest file using the Dropbox

#### Install GAWK Dependency
Ensure that you have the gawk package installed on your OS (apt-get install gawk)
```bash
sudo apt-get install gawk -y
```
#### Copy files to Destination Folders (from the scannerpi repo folder)
```bash
sudo cp dbpurge /usr/local/bin/dbpurge
sudo mkdir /etc/dbpurge
sudo cp dbpurge.conf /etc/dbpurge/dbpurge.conf   
```
#### Edit Permission & Ownership
```bash
sudo chmod 755 dbpurge
sudo chmod 644 dbpurge.conf
```
#### Finalize the Installation
Update the Pi's crontab
```bash
crontab -e
```
####
...and add the following lines
```bash
*/x * * * * /usr/local/bin/dbpurge > /home/pi/dbpurge/dbpurge.log 2>&1
```